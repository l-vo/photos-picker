from photospicker.picker.abstract_exif_date_picker import \
    AbstractExifDatePicker
import random
import math


class SmartPicker(AbstractExifDatePicker):
    """
    Pick intelligently photos depending on EXIF DateTimeOriginal
    The chance for a photo to be selected is proportional to its recency.
    Actually, the majority of retrieved photos will be recent and a few old
    photos will be also retrieved.
    """

    def scan(self):
        """Scan the given path for building picked file paths list"""
        sorted_filenames = self._build_sorted_filenames()
        for i in range(1, 21):
            ratio = i * .05
            ret = self._compute_packet_extractions(ratio, sorted_filenames)
            if ret is not None:
                break  # use the lowest ratio found

        (packet_size, extractions) = ret
        current_packet = []
        total = len(sorted_filenames)
        for key, filename in enumerate(sorted_filenames):
            current_packet.append(filename)
            k = key + 1
            if k % packet_size == 0 and total - k >= packet_size:
                self._process_packet(current_packet, extractions)
                current_packet = []

        if current_packet:
            self._process_packet(current_packet, extractions)

    def _process_packet(self, current_packet, extractions):
        """
        Randomly select photos inside a packet

        :param list current_packet: packet
        :param list extractions: list of photos count to extract of each packet
        """
        random.shuffle(current_packet)
        to_extract = extractions.pop(0)
        self._picked_file_paths += [
            x for key, x in enumerate(current_packet)
            if key < to_extract
        ]

    def _compute_packet_extractions(self, ratio, sorted_filenames):
        """
        Compute the successive photos count to extract from packets
        depending on the given ratio. Returns false if computing is
        not possible with self._photo_count and total photos count.

        :param float ratio: ratio
        :param list sorted_filenames: sorted filenames

        :return: None/tuple
        """
        remaining = min(self._photos_count, len(sorted_filenames))
        max_val = None
        extractions = []
        while remaining > 0:
            to_extract = int(max(round(remaining * ratio), 1))
            if max_val is None:
                # the first (and bigger) count
                # to extract must be greater than 1
                if to_extract < 2:
                    return None
                max_val = to_extract
            remaining -= to_extract
            extractions.append(to_extract)

        # Packets count is equal to extractions count
        packet_size = math.ceil(
            len(sorted_filenames) / float(len(extractions))
        )
        if packet_size < max_val:
            return None

        return (packet_size, extractions)
