import bcrypt
import os
import sys

def encrypt_password(clear_text_password):
    return bcrypt.hashpw(clear_text_password.encode(), bcrypt.gensalt()).decode()

def get_env_variables(variable_names):
    return {var: os.getenv(var) for var in variable_names}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python encrypt.py <ENV_VAR_1> <ENV_VAR_2> ...")
        sys.exit(1)

    env_var_names = sys.argv[1:]
    passwords = get_env_variables(env_var_names)

    encrypted_passwords = {key.replace('_CLEAR', ''): encrypt_password(value) for key, value in passwords.items() if value}

    for key, value in encrypted_passwords.items():
        print(f"{key}={value}")