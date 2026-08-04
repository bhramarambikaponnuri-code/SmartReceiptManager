from collections import defaultdict


def reconstruct_rows(results, y_threshold=20):
    """
    Reconstruct receipt rows while preserving horizontal spacing.
    """

    rows = defaultdict(list)

    for box, text, conf in results:

        xs = [p[0] for p in box]
        ys = [p[1] for p in box]

        x = min(xs)
        y = sum(ys) / len(ys)

        matched = None

        for existing in rows:
            if abs(existing - y) <= y_threshold:
                matched = existing
                break

        if matched is None:
            matched = y

        rows[matched].append((x, text))

    final_lines = []

    for y in sorted(rows.keys()):

        words = sorted(rows[y], key=lambda x: x[0])

        line = ""

        last_x = 0

        for x, text in words:

            gap = x - last_x

            # Add spaces based on X distance
            spaces = max(1, gap // 40)

            line += " " * int(spaces)
            line += text

            last_x = x + len(text) * 10

        final_lines.append(line.strip())

    return final_lines