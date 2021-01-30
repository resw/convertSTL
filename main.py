# -*- encoding: utf-8 -*-
import struct


def convet_binary_to_ascii():
    dosya_ismi = "kanat_profili"
    dosya_uzantisi = ".stl"
    binary_stl_file = open(dosya_ismi + dosya_uzantisi, 'rb')
    ascii_stl_file = open(dosya_ismi + '_ascii' + dosya_uzantisi, 'w')

    kati_ismi = dosya_ismi.upper()

    ascii_stl_file.write("solid " + kati_ismi)

    tab_str = "  "
    sayac_byte = 0
    sayac_nokta_byte = 0  # Her 12 olduğunda sıfırlanacak
    while True:
        if sayac_byte < 80:
            byte = binary_stl_file.read(1)
            # print(byte)

            if not byte == b'\x00':
                byte_read = struct.unpack('c', byte)[0]
                # ascii_stl_file.write(byte_read.decode(encoding))

            sayac_byte = sayac_byte + 1

        elif sayac_byte < 84:
            byte = binary_stl_file.read(4)
            faces = struct.unpack('I', byte)[0]
            # print("STL Yüz Sayısı: " + str(faces))

            sayac_byte = sayac_byte + 4

        elif sayac_byte >= 84:
            byte = binary_stl_file.read(4)

            if byte == b'':
                break
            else:
                nokta = struct.unpack('f', byte)[0]
                if nokta == 0:
                    nokta = 0  # -0.0 ve +0.0 olayını önlemek için
                nokta_str = ' {:.6e}'.format(nokta)

                if sayac_nokta_byte == 0:
                    ascii_stl_file.write("\n" + tab_str + "facet normal")
                    ascii_stl_file.write(nokta_str)

                elif sayac_nokta_byte < 11:
                    if sayac_nokta_byte == 3:
                        ascii_stl_file.write("\n" + 2 * tab_str + "outer loop")
                        ascii_stl_file.write("\n" + 3 * tab_str + "vertex")
                    elif sayac_nokta_byte == 6:
                        ascii_stl_file.write("\n" + 3 * tab_str + "vertex")
                    elif sayac_nokta_byte == 9:
                        ascii_stl_file.write("\n" + 3 * tab_str + "vertex")

                    ascii_stl_file.write(nokta_str)

                elif sayac_nokta_byte == 11:
                    ascii_stl_file.write(nokta_str)
                    ascii_stl_file.write("\n" + 2 * tab_str + "endloop")
                    ascii_stl_file.write("\n" + tab_str + "endfacet")

                    sayac_nokta_byte = -1
                    byte = binary_stl_file.read(2)  # Boş byte alanlarını oku ve imleci ileri al

                sayac_nokta_byte = sayac_nokta_byte + 1
                sayac_byte = sayac_byte + 4

        else:
            break

    ascii_stl_file.write("\nendsolid " + kati_ismi)
    ascii_stl_file.close()
    print("İşlem Tamam")


if __name__ == '__main__':
    convet_binary_to_ascii()
