# -*- coding: utf-8 -*-
""" Prime polynomial cipher analysis

There is no real explanation for the 83 long cipher alphabet was choose, but we
can note that's a prime number.

We use here the first cryptography manual of Friedman
as main reference for terms and methodology:
https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/military-cryptanalysis/mil_crypt_I.pdf

One explanation would be the cipher is `c[i] = (k[i] * p[i] + phi) % 83`, in
that case :
    - it's explaining why a prime number is chosen as modulo
    - as long `k` values are prime, not in `p`, and k[i] != k[i+1], they can't
    have double following letters on the cryptogram.

We don't know what is the size of `k`, but as `(a*b)%n = ((a%n)*(b%n))%n`, we
can only consider primes under 83.

In this script we will:
    - Proove that there is a set of k and p where c can have 0-82 values
    - Decrypt for all possibilities and check all values

Even if I'm the father of this formula, @Toboter did help me a lot on this on,
as he did the algorithm to find prim with less plaintext range, in a very
efficient manner.
"""
import time
import random
from collections import deque

from tqdm import tqdm

from constant.message import eyes_messages
from analysis.ioc import ioc
from utils.notify import beep

MODULO = 83
PRIMES = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79]

def get_primes_between(min=0, max=MODULO) -> list[int]:
    """ Returns primes in betweens [min;max[ """
    return [p for p in PRIMES if p >= min and p < max]

# Bruteforce
def decrypt(key, phi, message) -> list[int]:
    """ Decrypt the message as `c[i] = (k[i] * p[i] + phi) % 83`
    
    Return:
        (list[int]) plain text
    """

    plain = deque()
    for i in range(len(message)):
        for j in range(MODULO):
            if ((key[i] * j + phi) % MODULO) == message[i]:
                plain.append(j)
                break

    return list(plain)

def generator_key(elements, size=1) -> "tuple(list[int], int)":
    """ Yield each possible key as key[i] != key[i+1]

    Note that the possibilities are `len(elements) ** size`.
    As it can be implement as a number of base `len(elements)`.

    Will skip key with double
    Will skip key that doesn't include the last element of "elements"
    
    Return:
        (list[int], int) key values, along with the number of skipped keys
    """
    if not elements:
        return

    # Elements index per key index (= number of base `len(elements)`)
    elements_indexes = [0]*size # [[i % 2] for i in range(size)]

    # If the key index is not in the `elements_indexes`
    # The `elements_indexes` for a solution that is include in
    # another set of element. No need to test a key twice
    key_index = len(elements)-1

    # Generate keys
    skipped_keys = 0
    for _ in range(len(elements) ** size):

        # Compute the next index and check for double
        found_double = False
        found_key_index = False
        end_reach = False
        elements_indexes[0]+=1
        for j, v in enumerate(elements_indexes):
            # Increment indexes
            if v == len(elements) and j != size-1:
                elements_indexes[j] = 0
                elements_indexes[j+1] += 1

            if elements_indexes[j] == key_index:
                found_key_index = True

            # Check for double
            if (
                j != 0
                and elements_indexes[j-1] == elements_indexes[j]
            ) or (
                j != size-1
                and elements_indexes[j+1] == elements_indexes[j]
            ):
                found_double=True
            
            # Break if need (opti)
            if (end_reach and found_key_index) or found_double:
                break
        
        # Double are skip
        if found_double or not found_key_index:
            skipped_keys += 1
            continue

        yield ([elements[j] for j in elements_indexes], skipped_keys,)
        skipped_keys = 0  # Reset count
    return

if __name__ == '__main__':
    # Proof of [There is a set of k and p where c can have 0-82 values].
    valid_cursors = []
    for cursor in range(MODULO):
        map_is_reach = {symbol: False for symbol in range(MODULO)}
        for p in range(0, cursor):
            for k in get_primes_between(min=cursor):
                map_is_reach[(p * k) % MODULO] = True
        
        if all(map_is_reach.values()):
            valid_cursors.append(cursor)

    # minP = []
    # for i in range(200):
    #     nmp = 100
    #     for j in range(1,83):
    #         ps = []
    #         for m in messages:
    #             if len(m)>i:
    #                 ps.append( (m[i] * j) % 83)

    #         if ps:
    #             p = max(ps)
    #             if p < nmp:
    #                 nmp = p

    #     if nmp < 100:
    #         minP.append(nmp)
    # print(max(minP))

    # Cleaning cursors (in between primes values) values are following each other.
    # Not that cursor on 73 and 79 lead to no possible keys
    valid_cursors = [p for p in PRIMES if p in valid_cursors]
    valid_cursors = [c for c in valid_cursors if c > 36]  # 36 = A-Z + 0-9
    # valid_cursors = [c for c in valid_cursors if c > 47] # 61 from Toboter check
    # valid_cursors = [61] # from Toboter check

    # Settings
    BRUTE_CHUNK = 7      # Number of char check
    BRUTE_OFFSET = 25    # Offset from begin of each message
    BRUTE_KEEP = 5       # Top of values keep at each chunk
    # Number of iteration to cover the smaller message chunk by chunk
    BRUTE_ITER_COUNT = (
        min([len(m) for m in eyes_messages])-BRUTE_OFFSET
    ) // BRUTE_CHUNK

    # Define out random base
    random_buffer = deque()
    for _ in tqdm(range(10000)):
        random_buffer.append(ioc([random.randint(0, MODULO) for _ in range(BRUTE_CHUNK)]))
    ioc_random = sum(random_buffer)/len(random_buffer)

    # Define out control
    plain_control = None
    with open("./analysis/control.txt", "r", encoding="utf-8") as control_file:
        plain_control = control_file.read().lower()
    ioc_control = ioc(list(plain_control))

    # TIME TO BRRRRRRRRRRRRRRRRRRRRRRRRRRR
    top_solutions_per_chunk = []
    for n, cursor in enumerate(valid_cursors[::-1]):
        # Compute all possibilities and sort them by IoC
        key_elements = get_primes_between(min=cursor)
        with tqdm(total=BRUTE_ITER_COUNT * (len(key_elements) ** BRUTE_CHUNK)) as pbar:
            pbar.set_description(
                f"Brute keys for primes in [{cursor}, 83[ ({n:02d}/{len(valid_cursors[::-1])})"
            )
            for chunk_id in range(BRUTE_ITER_COUNT):
                iocs_chunk = deque()
                
                for key, skipped_keys in generator_key(
                    key_elements,
                    size=BRUTE_CHUNK,
                ):
                    plain_message_encoded = []
                    for eye_message in eyes_messages:
                        plain_message_encoded += decrypt(
                            key,
                            0,
                            eye_message[
                                BRUTE_OFFSET+BRUTE_CHUNK*chunk_id
                                :BRUTE_OFFSET+BRUTE_CHUNK*(chunk_id+1)
                            ],
                        )

                    iocs_chunk.append((
                        cursor,
                        0,
                        key,
                        ioc(plain_message_encoded)/ioc_random,
                        plain_message_encoded,
                    ))

                    pbar.update(1 + skipped_keys)

                iocs_chunk = sorted(iocs_chunk, key=lambda x: -x[3])
                with open(f"./output/prime_polynomial.{cursor}.{chunk_id}.txt", "w", encoding="utf-8") as f:
                    for cursor, phi, key, _ioc, plain in iocs_chunk:
                        f.write(f'{cursor}\t{phi}\t{key}\t{_ioc:.3f}\t' + ''.join([chr(p+32) for p in plain]).replace('\n', ' ') + "\n")
                
                top_solutions_per_chunk.append(iocs_chunk[:BRUTE_KEEP])
                # # Bypass for faster debug
                # for chunk_id in range(BRUTE_ITER_COUNT):
                #     top_solutions_per_chunk.append(iocs_chunk[:BRUTE_KEEP])
                # break # for faster debug
        
        # Notify user we finish chunks
        beep(".._ " * 4)

        # No values ? no merge required
        if not top_solutions_per_chunk:
            continue

        """ Merge chunks
        Assemble top set of each chunk
        Test all possibilities
        Sort by IoC and store them in a file
        """

        # chunk_indexes = number of base `len(top_solutions_per_chunk`
        # (max: BRUTE_KEEP)
        chunk_indexes = [0] * len(top_solutions_per_chunk)

        # Progress bar related
        combinations_count = len(top_solutions_per_chunk[0]) ** len(top_solutions_per_chunk)
        tdqm_description = f"Merge for {cursor} ({n:02d}/{len(valid_cursors[::-1])})"
        progess_bar = tqdm(
            range(combinations_count),
            desc=tdqm_description,
        )

        chunk_merge_buffer = deque()
        merge_dump_file_id = 0 # For dump file
        for m in progess_bar:
            # Compute the next index
            chunk_indexes[0]+=1
            for j, v in enumerate(chunk_indexes):
                # Increment indexes
                if v == len(top_solutions_per_chunk[j]) and j != len(top_solutions_per_chunk)-1:
                    chunk_indexes[j] = 0
                    chunk_indexes[j+1] += 1
                else:
                    # Break if no more update (opti)
                    break

            # Concat to a single list (= plaintext encoded)
            plaintext = []
            for j, v in enumerate(chunk_indexes):
                try:
                    plaintext += top_solutions_per_chunk[j][v][4]
                except:
                    print("GOD DAMN IT")
                    print(chunk_indexes)
                    print(f"len(top_solutions_per_chunk) = {len(top_solutions_per_chunk)}")
                    if j < len(top_solutions_per_chunk):
                        print(f"len(top_solutions_per_chunk[j]) = {len(top_solutions_per_chunk[j])}")
                        if v < len(top_solutions_per_chunk[j]):
                            print(f"len(top_solutions_per_chunk[j][v]) = {len(top_solutions_per_chunk[j][v])}")
            chunk_merge_buffer.append((ioc(plaintext), plaintext, list(chunk_indexes)))

            # Each 1M, dump into a file and reset the buffer
            if (m % (10**6)) == 0 or m == combinations_count -1:
                progess_bar.set_description(
                    f"Save merge result for {cursor} "
                    f"({n:02d}/{len(valid_cursors[::-1])})"
                )
                # Sort and save results for this cursor
                chunk_merge_buffer = sorted(chunk_merge_buffer, key=lambda x: -x[0])
                with open(
                    (
                        f"./output/prime_polynomial.{cursor}.top."
                        f"{merge_dump_file_id}.txt"
                    ),
                    "w",
                    encoding="utf-8",
                ) as dump_file:
                    for _ioc, plain, indexes  in chunk_merge_buffer:
                        dump_file.write(f'{_ioc}\t{indexes}\t' + ''.join([chr(p+32) for p in plain]).replace('\n', ' ') + "\n")
                
                # Increase the id for file name and reset buffer
                merge_dump_file_id += 1
                chunk_merge_buffer = deque()
                progess_bar.set_description(tdqm_description)
        beep("._.__ " * 4)

    beep("......")
    print(" ==== OK ==== ")
    print(f"control : {ioc_control}")
    print(f"random : {ioc_random}")