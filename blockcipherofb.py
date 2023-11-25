def Block_Binary(text, block_sizes = 8):

  modulo = len(text) % block_sizes
  if(modulo != 0):
    modulo = '0' * (block_sizes - modulo)
    text = modulo + text

  return [text[i:i + block_sizes] for i in range(0, len(text), block_sizes)]

def Xor_Blocks(block1, block2):
  return ''.join(str(int(a) ^ int(b)) for a, b in zip(block1, block2))

# Menggeser sebanyak 1 bit kekiri dan mengisi kekosongan dengan 1 bit dari cipher text
def Shift_Left(initialize_vector, cipher_text):
  return initialize_vector[1:] + cipher_text[0]

def Shift_Right(initialize_vector, cipher_text):
  return cipher_text[-1] + initialize_vector[:-1]


def encrypt(plain_text, key, init_vector = None, len_bit = 8):
  len_bit = int(len_bit)

  if init_vector == None or init_vector == '':
    init_vector = ''
    for x in range(len_bit):
      init_vector += '0'
  # else:
  #   init_vector = ''.join(format(ord(char), '08b') for char in init_vector)
  # Konversi teks ke dalam biner dengan padding jika perlu
  plain_text = ''.join(format(ord(char), '08b') for char in plain_text)
  key = ''.join(format(ord(char), '08b') for char in key)

  print(len(plain_text))
  # Blocking binary, blocking default = 8
  plain_block = Block_Binary(plain_text, len_bit)
  key_block = Block_Binary(key, len_bit)
  init_vector_block = Block_Binary(init_vector, len_bit)

  encrypt_biner = ''
  encrypt_hex = ''
  encrypt_text = ''

  i = 0
  j = 0
  for i, block in enumerate(plain_block):
    if i >= len(key_block):
      i = 0
    # XOR dari IV dan koentji
    xor_IV = Xor_Blocks(init_vector_block[0], key_block[i])
    if(j<=2):
      print(f"Nilai IV {init_vector_block[0]}")
      print(f"nilai key {i+1} {key_block[i]}")
      print(f"Hasil XOR IV dengan key {i+1} {xor_IV}")

    i += 1

    # Geser ke kiri AJA buat geser
    # xor_IV = xor_IV[2:] + xor_IV[0] + xor_IV[1]
    # Geser ke kanan AJA buat geser
    xor_IV = xor_IV[-0] + xor_IV[-1] + xor_IV[:-2]
    if(j<=2):
      print(f"nilai xor IV setelah shifting {xor_IV}")

    # Proses enkripsi XOR dari tiap block plain text dan hasil xor IV
    xor_result = Xor_Blocks(block, xor_IV)
    if(j<=2):
      print(f"nilai block original {block}")
      print(f"Blok ke-{i+1} Enkripsi XOR (C{i+1}): {xor_result} \n")

    j += 1
    # Geser ke kiri terus ambil dari xor IV nya paling kiri
    # init_vector_block[0] = Shift_Left(init_vector_block[0], xor_IV)
    # Geser ke kanan terus ambil dari xor IV nya paling kanan
    init_vector_block[0] = Shift_Right(init_vector_block[0], xor_IV)

    encrypt_biner += xor_result
  encrypt_hex = hex(int(encrypt_biner, 2))[2:]
  # encrypt_text = [chr(int(encrypt_biner[i:i+8], 2)) for i in range(0, len(plain_text), 8)]
  print(f"Hasil enkripsi binary {encrypt_biner}")
  print(f"Hasil enkripsi hexadecimal {encrypt_hex}")
  # print(f"Hasil enkripsi char {encrypt_text}")

  return encrypt_hex, encrypt_biner

def decrypt(cipher_text_hex, key, init_vector = None, len_bit=8):
  len_bit = int(len_bit)
  if init_vector == None or init_vector == '':
    init_vector = ''
    for x in range(len_bit):
      init_vector += '0'
  # else:
  #   init_vector = ''.join(format(ord(char), '08b') for char in init_vector)
  key = ''.join(format(ord(char), '08b') for char in key)

  cipher_block = Block_Binary(cipher_text_hex, len_bit)
  key_block = Block_Binary(key, len_bit)
  init_vector_block = Block_Binary(init_vector, len_bit)
  plain_text = ''

  i = 0
  j = 0
  for i, block in enumerate(cipher_block):
    if i >= len(key_block) :
      i = 0
    # XOR dari IV dan koentji
    xor_IV = Xor_Blocks(init_vector_block[0], key_block[i])
    if(j<=2):
      print(f"Nilai IV {init_vector_block[0]}")
      print(f"Nilai key {key_block[i]}")
      print(f"Hasil XOR IV dengan key {xor_IV}")

    i += 1

    # Geser ke kiri AJA buat geser
    # xor_IV = xor_IV[2:] + xor_IV[0] + xor_IV[1]
    # Geser ke kanan AJA buat geser
    xor_IV = xor_IV[-0] + xor_IV[-1] + xor_IV[:-2]
    if(j<=2):
      print(f"Nilai xor IV setelah shifting {xor_IV}")

    xor_decrypt = Xor_Blocks(block, xor_IV)
    if(j<=2):
      print(f"Nilai block original {block}")
      print(f"Blok ke-{i+1} Plain Text XOR (P{i+1}): {xor_decrypt} \n")

    j += 1
    # Geser kiri tapi ambil value dari hasil xor dari initialize vector 1 bit paling kiri
    # init_vector_block[0] = Shift_Left(init_vector_block[0], xor_IV)
    # Geser ke kanan terus ambil dari xor IV nya paling kanan
    init_vector_block[0] = Shift_Right(init_vector_block[0], xor_IV)

    plain_text += xor_decrypt
  hexa_plain = hex(int(plain_text, 2))[2:]
  characters = "".join([chr(int(hexa_plain[i:i+2], 16)) for i in range(0, len(hexa_plain), 2)])
  print(plain_text)
  plain_text = ''.join(characters)
  return plain_text

def main():
  jumlah_bits = 8
  IV = None
  while True:
        print("\nPilihlah salah satu dari pilihan berikut:")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Custom jumlah bit")
        print("4. Keluar dari program")
        choice = input("Masukkan pilihan Anda: ")

        if choice == '1':
            plain_text = input("Masukkan plain text: ")
            key = input("Masukkan kunci: ")
            IV = input("Masukkan Initialize vector (sesuai custom bit): ")
            hex_cipher_text, cipher_text = encrypt(plain_text, key, IV,len_bit=jumlah_bits)
        elif choice == '2':
            cipher_text = input("Masukkan cipher text (dalam heksadesimal): ")
            key = input("Masukkan kunci: ")
            cipher_text_bin = bin(int(cipher_text, 16))[2:].zfill(len(cipher_text)*4)
            print(cipher_text_bin)
            plain_text = decrypt(cipher_text_bin, key, IV, len_bit=jumlah_bits)
            print("Plain Text:", plain_text)
        elif choice == '3':
            jumlah_bits = input("Custom nilai bit mu: (default = 8)")
        elif choice == '4':
            print("Terima kasih, program selesai.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih 1, 2, atau 3.")



main()