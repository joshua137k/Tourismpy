


def adjust_text_to_fit(text, max_width, font):
    """
    Ajusta o texto para caber dentro de um dado limite de largura.
    Se o texto for muito longo, ele é reduzido e termina com elipses.
    """
    text_surface = font.render(text, True, (0,0,0))
    text_width = text_surface.get_width()
    # Se o texto couber, retorne-o como está.
    if text_width <= max_width:
        return text
    # Reduza o texto até que ele caiba.
    while text_width > max_width and len(text) > 0:
        text = text[:-1]
        text_surface = font.render(text + '...', True,(0,0,0))
        text_width = text_surface.get_width()
    return text + '...'
