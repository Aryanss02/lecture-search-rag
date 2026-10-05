import re


# ---------------------------------------------------------
# Convert timestamp → seconds
#
# Supports:
# 02:40
# 1:06
# 5:12:47
# ---------------------------------------------------------

def timestamp_to_seconds(timestamp):

    parts = timestamp.split(":")

    if len(parts) == 2:

        minutes = int(parts[0])
        seconds = int(parts[1])

        return minutes * 60 + seconds

    elif len(parts) == 3:

        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])

        return hours * 3600 + minutes * 60 + seconds

    else:

        raise ValueError(
            f"Invalid timestamp: {timestamp}"
        )


# ---------------------------------------------------------
# Create YouTube URL with timestamp
# ---------------------------------------------------------

def create_timestamp_url(video_url, seconds):

    separator = "&" if "?" in video_url else "?"

    return f"{video_url}{separator}t={seconds}s"


# ---------------------------------------------------------
# Clean transcript text
# ---------------------------------------------------------

def clean_transcript_text(text):

    text = text.strip()

    # Remove the duplicated human-readable timestamp.
    #
    # Example:
    #
    # "8 secondsIf you want..."
    # → "If you want..."
    #
    # "1 minute, 6 secondsalmost every..."
    # → "almost every..."
    #
    # "5 hours, 12 minutes, 47 secondsthen they..."
    # → "then they..."

    text = re.sub(
        r"^\d+\s*"
        r"(?:seconds?|minutes?|hours?)"
        r"(?:,\s*\d+\s*"
        r"(?:seconds?|minutes?|hours?))*",
        "",
        text,
        flags=re.IGNORECASE
    )

    return text.strip()


# ---------------------------------------------------------
# Parse lecture file
# ---------------------------------------------------------

def read_lecture(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        lines = file.readlines()

    video_url = None
    video_title = None

    segments = []

    current_timestamp = None
    current_text = []

    waiting_for_title = False

    # -----------------------------------------------------
    # Read every line
    # -----------------------------------------------------

    for line in lines:

        line = line.strip()

        # Ignore empty lines
        if not line:
            continue

        # -------------------------------------------------
        # Get video URL
        # -------------------------------------------------

        if line.startswith("VIDEO_URL="):

            video_url = line.split(
                "=",
                1
            )[1].strip()

            continue

        # -------------------------------------------------
        # Get video title
        # -------------------------------------------------

        if line.startswith("VIDEO_TITLE="):

            title_value = line.split(
                "=",
                1
            )[1].strip()

            if title_value:

                video_title = title_value
                waiting_for_title = False

            else:

                waiting_for_title = True

            continue

        # -------------------------------------------------
        # Handle title on next non-empty line
        # -------------------------------------------------

        if waiting_for_title:

            video_title = line
            waiting_for_title = False

            continue

        # -------------------------------------------------
        # Detect timestamp at beginning of line
        #
        # Examples:
        #
        # 0:000 seconds...
        # 1:061 minute, 6 seconds...
        # 5:12:475 hours, 12 minutes, 47 seconds...
        #
        # IMPORTANT:
        # The regex checks for:
        #
        # H:MM:SS
        # OR
        # M:SS
        # -------------------------------------------------

        timestamp_match = re.match(
            r"^(\d{1,2}:\d{2}:\d{2}|\d{1,2}:\d{2})(.*)$",
            line
        )

        if timestamp_match:

            # -------------------------------------------------
            # Save previous segment
            # -------------------------------------------------

            if current_timestamp is not None:

                start_seconds = timestamp_to_seconds(
                    current_timestamp
                )

                segments.append({
                    "timestamp": current_timestamp,
                    "start_time": start_seconds,
                    "text": " ".join(current_text)
                })

            # -------------------------------------------------
            # Extract timestamp
            # -------------------------------------------------

            current_timestamp = timestamp_match.group(1)

            # -------------------------------------------------
            # Extract transcript text
            # -------------------------------------------------

            remaining_text = timestamp_match.group(2)

            remaining_text = clean_transcript_text(
                remaining_text
            )

            current_text = []

            if remaining_text:

                current_text.append(
                    remaining_text
                )

        else:

            # -------------------------------------------------
            # Normal transcript line
            # -------------------------------------------------

            current_text.append(line)

    # -----------------------------------------------------
    # Save final segment
    # -----------------------------------------------------

    if current_timestamp is not None:

        start_seconds = timestamp_to_seconds(
            current_timestamp
        )

        segments.append({
            "timestamp": current_timestamp,
            "start_time": start_seconds,
            "text": " ".join(current_text)
        })

    # -----------------------------------------------------
    # Calculate end time
    # -----------------------------------------------------

    for i in range(len(segments)):

        if i + 1 < len(segments):

            segments[i]["end_time"] = (
                segments[i + 1]["start_time"]
            )

        else:

            segments[i]["end_time"] = (
                segments[i]["start_time"]
            )

    # -----------------------------------------------------
    # Add video information
    # -----------------------------------------------------

    for segment in segments:

        segment["video_url"] = video_url

        segment["video_title"] = video_title

        segment["timestamp_url"] = (
            create_timestamp_url(
                video_url,
                segment["start_time"]
            )
        )

    # -----------------------------------------------------
    # Return parsed lecture
    # -----------------------------------------------------

    return {
        "video_url": video_url,
        "video_title": video_title,
        "segments": segments
    }