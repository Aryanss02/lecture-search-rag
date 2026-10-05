CHUNK_DURATION = 75


def create_chunks(segments):

    chunks = []

    current_segments = []
    chunk_start = None

    for segment in segments:

        # First segment of a new chunk
        if chunk_start is None:
            chunk_start = segment["start_time"]

        current_segments.append(segment)

        # Calculate current chunk duration
        current_duration = (
            segment["end_time"] - chunk_start
        )

        # Create chunk once we reach 75 seconds
        if current_duration >= CHUNK_DURATION:

            chunks.append(
                build_chunk(current_segments)
            )

            current_segments = []
            chunk_start = None

    # Add remaining segments
    if current_segments:

        chunks.append(
            build_chunk(current_segments)
        )

    return chunks


def build_chunk(segments):

    first = segments[0]
    last = segments[-1]

    # Combine all transcript text
    text = " ".join(
        segment["text"]
        for segment in segments
    )

    return {
        "text": text,

        "video_title": first["video_title"],

        "video_url": first["video_url"],

        "start_time": first["start_time"],

        "end_time": last["end_time"],

        "timestamp_url": first["timestamp_url"]
    }