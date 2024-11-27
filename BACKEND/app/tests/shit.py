from random import choice, sample

def gen_rand_email():
    alphas = [*"a b c d e f g h i j k l m n o p q r s t u v w x y z _".split(' ')]
    email = "".join(sample(alphas, k=8)) + "@example.com"
    return email

print(gen_rand_email())