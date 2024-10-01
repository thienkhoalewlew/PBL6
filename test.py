def mod_pow(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def encrypt_rsa():
    print("Chương trình mã hóa RSA đơn giản")
    m = int(input("Nhập thông điệp m: "))
    e = int(input("Nhập số mũ công khai e: "))
    n = int(input("Nhập modulo n: "))
    
    c = mod_pow(m, e, n)
    
    print(f"Bản mã c = {c}")

if __name__ == "__main__":
    encrypt_rsa()