import numpy as np
from publicmodel.common import ord2, chr2, animation_progress_bar, auto_line_wrap
from pydub import AudioSegment


def one_layer_encryption(text):
    try:
        return ord2(text)
    except ValueError:
        pass


def second_level_decryption(text):
    try:
        return chr2(text)
    except ValueError:
        pass


class Encryptor:
    def __init__(self, text, carrier_audio_path):
        self.text = one_layer_encryption(text) + "<END>"  # 添加结束标志
        self.carrier_audio_path = carrier_audio_path
        self.sample_rate, self.carrier_audio = self.read_audio(carrier_audio_path)
        self.text_bits = self.text_to_bits(self.text)

    def read_audio(self, path):
        audio = AudioSegment.from_file(path)
        audio = audio.set_channels(1)  # 转换为单声道
        samples = np.array(audio.get_array_of_samples())
        return audio.frame_rate, samples

    def text_to_bits(self, text):
        bits = ''.join(format(ord(char), '08b') for char in text)
        return bits

    def hide_text_in_audio(self):
        audio_data = self.carrier_audio.copy()
        bit_index = 0
        for i in range(len(audio_data)):
            if bit_index < len(self.text_bits):
                audio_data[i] = (audio_data[i] & ~1) | int(self.text_bits[bit_index])
                bit_index += 1
        return audio_data

    def save_audio(self):
        audio_data = self.hide_text_in_audio()
        audio_segment = AudioSegment(
            audio_data.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=audio_data.dtype.itemsize,
            channels=1
        )
        audio_segment.export(self.carrier_audio_path, format="wav")


class Decryptor:
    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.sample_rate, self.audio_data = self.read_audio(audio_path)

    def read_audio(self, path):
        audio = AudioSegment.from_file(path)
        audio = audio.set_channels(1)  # 转换为单声道
        samples = np.array(audio.get_array_of_samples())
        return audio.frame_rate, samples

    def bits_to_text(self, bits):
        chars = [chr(int(bits[i:i + 8], 2)) for i in range(0, len(bits), 8)]
        return ''.join(chars)

    def audio_to_text(self):
        bits = ''
        for i in range(len(self.audio_data)):
            bits += str(self.audio_data[i] & 1)
        text = self.bits_to_text(bits)
        end_index = text.find("<END>")
        if end_index != -1:
            text = text[:end_index]
        return second_level_decryption(text)


if __name__ == '__main__':
    text = (
        'This encryption method embeds text into audio files using bit manipulation. The text is first encrypted with '
        'a custom function and appended with "<END>". The audio file is converted to mono and its samples are modified '
        'to hide the text bits. The modified audio is saved as a WAV file. For decryption, the audio file is read, and '
        'the hidden bits are extracted and converted back to text, stopping at "<END>". The text is then decrypted '
        'using the custom function.'
    )

    encryptor = Encryptor(
        text,
        '../../audio/hide_to_audio_lite.wav'
    )
    animation_progress_bar(
        "Encrypting...",
        None,
        0.25,
        encryptor.save_audio,
        "process",
    )
    print("Encryption is complete.")

    decryptor = Decryptor('../../audio/hide_to_audio_lite.wav')
    extracted_text = animation_progress_bar(
        "Decrypting...",
        None,
        0.25,
        decryptor.audio_to_text,
        "process",
    )
    try:
        extracted_text = auto_line_wrap(extracted_text, 100, True)
    except AttributeError:
        pass

    print("Decryption is completed.\n")
    print("Decrypted text:")
    print(extracted_text)
