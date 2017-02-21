# -*- coding: utf-8 -*-
__author__ = 'Дмитрий'
import hashlib

def generate_password_hash(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()

def check_password_hash(password_hash, password):
    return password_hash == generate_password_hash(password)