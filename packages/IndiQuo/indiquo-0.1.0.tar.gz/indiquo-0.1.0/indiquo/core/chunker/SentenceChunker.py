import math
from typing import List

from indiquo.core.chunker.BaseChunker import BaseChunker
from indiquo.core.chunker.Chunk import Chunk
import pysbd
import re


class SentenceChunker(BaseChunker):

    def __init__(self, min_length: int = 0, max_length: int = 10000, max_sentences: int = 25):
        self.min_length = min_length
        self.max_length = max_length
        self.max_sentences = max_sentences

    # overriding abstract method
    def chunk(self, text: str) -> List[Chunk]:
        seg = pysbd.Segmenter(language="de", clean=False, char_span=True)
        text_spans = seg.segment(text)

        chunks_1 = []

        # fix number and brackets
        for ts in text_spans:
            match = re.search(r'^\(.{1,25}\)', ts.sent.strip())

            if match:
                last_chunk = chunks_1[-1]
                last_chunk.text += ts.sent
                last_chunk.end = ts.end
            else:
                chunks_1.append(Chunk(ts.start, ts.end, ts.sent))

        current_chunk = None
        current_length = 0
        chunks_2 = []
        chunk_count = 0

        for c_pos, c in enumerate(chunks_1):
            chunk_count += 1

            if current_length == 0:
                current_chunk = Chunk(c.start, c.end, c.text)
                current_length = len(c.text.split())

                if current_length >= self.max_length:
                    if current_length == self.max_length:
                        chunks_2.append(current_chunk)
                    else:
                        chunks_2.extend(self.__split_too_long(current_chunk, current_length))

                    current_chunk = None
                    current_length = 0
                    chunk_count = 0
            else:
                next_length = len(c.text.split())

                if current_length + next_length == self.max_length:
                    current_chunk.text += c.text
                    current_chunk.end = c.end
                    chunks_2.append(current_chunk)
                    current_chunk = None
                    current_length = 0
                    chunk_count = 0
                elif current_length + next_length < self.max_length:
                    current_chunk.text += c.text
                    current_chunk.end = c.end
                    current_length += next_length
                else:
                    chunks_2.append(current_chunk)
                    current_chunk = Chunk(c.start, c.end, c.text)
                    current_length = next_length
                    chunk_count = 1

                    if current_length >= self.max_length:
                        if current_length == self.max_length:
                            chunks_2.append(current_chunk)
                        else:
                            chunks_2.extend(self.__split_too_long(current_chunk, current_length))

                        current_chunk = None
                        current_length = 0
                        chunk_count = 0

            if chunk_count >= self.max_sentences:
                if self.min_length == 0 or current_length >= self.min_length:
                    if current_chunk:
                        chunks_2.append(current_chunk)

                    chunk_count = 0
                    current_chunk = None
                    current_length = 0

        if current_chunk:
            chunks_2.append(current_chunk)

        return chunks_2

    def __split_too_long(self, chunk: Chunk, length: int) -> List[Chunk]:
        org_text = chunk.text
        factor = (length // self.max_length) + 1
        words = org_text.split()
        sub_length = math.ceil(len(words) / factor)
        parts = [words[i:i + sub_length] for i in range(0, len(words), sub_length)]
        start = chunk.start

        result = []
        for p in parts:
            p_text = ' '.join(p)
            end = start + len(p_text)
            result.append(Chunk(start, end, p_text))
            # add 1 for space
            start = end + 1

        # TODO: () must not be at be start of a chunk

        return result
