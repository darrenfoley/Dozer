import random


class Insult:
    _adjective_list = [
        'dirty',
        'soggy',
        'filthy',
        'slippery',
        'slimy'
    ]

    _noun_list = [
        'rascal',
        'simpleton',
        'cucumber',
        'monkey butt',
        'chihuahua'
    ]

    @classmethod
    def random(cls):
        return f'{random.choice(cls._adjective_list)} {random.choice(cls._noun_list)}'


class EightBall:
    _list = [
        "it is certain.",
        "it is decidedly so.",
        "without a doubt.",
        "yes - definitely.",
        "you may rely on it.",
        "as I see it, yes.",
        "most likely.",
        "outlook good.",
        "yes.",
        "signs point to yes.",
        "reply hazy, try again.",
        "ask again later.",
        "better not tell you now.",
        "cannot predict now.",
        "concentrate and ask again.",
        "don't count on it.",
        "my reply is no.",
        "my sources say no.",
        "outlook not so good.",
        "very doubtful."
    ]

    @classmethod
    def random(cls):
        return random.choice(cls._list)
