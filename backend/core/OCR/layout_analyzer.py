import json
from pathlib import Path


# =====================================================
# Layout Analyzer (v2 - rule based)
# =====================================================

class LayoutAnalyzer:

    def __init__(self,
                 y_threshold=15,
                 x_threshold=25,
                 min_table_rows=2):

        self.y_threshold = y_threshold
        self.x_threshold = x_threshold
        self.min_table_rows = min_table_rows


    # --------------------------------------------------
    # Utils
    # --------------------------------------------------

    def _get_center(self, bbox):

        xs = [p[0] for p in bbox]
        ys = [p[1] for p in bbox]

        cx = sum(xs) / 4
        cy = sum(ys) / 4

        return cx, cy


    def _sort_items(self, items):

        return sorted(
            items,
            key=lambda it: self._get_center(it["bbox"])[::-1]
        )


    # --------------------------------------------------
    # Group to lines
    # --------------------------------------------------

    def group_lines(self, items):

        lines = []

        for item in self._sort_items(items):

            _, cy = self._get_center(item["bbox"])

            added = False

            for line in lines:

                if abs(line["y"] - cy) < self.y_threshold:

                    line["items"].append(item)
                    added = True
                    break


            if not added:

                lines.append({
                    "y": cy,
                    "items": [item]
                })


        # sort inside each line by X
        for line in lines:

            line["items"].sort(
                key=lambda it: self._get_center(it["bbox"])[0]
            )


        return lines


    # --------------------------------------------------
    # Table detection
    # --------------------------------------------------

    def detect_tables(self, lines):

        tables = []


        def similar_x(l1, l2):

            if len(l1) != len(l2):
                return False

            for a, b in zip(l1, l2):

                x1, _ = self._get_center(a["bbox"])
                x2, _ = self._get_center(b["bbox"])

                if abs(x1 - x2) > self.x_threshold:
                    return False

            return True


        i = 0

        while i < len(lines) - 1:

            cur = lines[i]["items"]
            nxt = lines[i + 1]["items"]


            if similar_x(cur, nxt):

                block = [cur, nxt]

                i += 2

                while i < len(lines):

                    ln = lines[i]["items"]

                    if similar_x(block[-1], ln):
                        block.append(ln)
                        i += 1
                    else:
                        break


                if len(block) >= self.min_table_rows:
                    tables.append(block)

            else:
                i += 1


        return tables


    # --------------------------------------------------
    # Analyze 1 page
    # --------------------------------------------------

    def analyze_page(self, ocr_data):

        items = ocr_data["items"]

        lines = self.group_lines(items)

        tables = self.detect_tables(lines)


        blocks = []

        used_lines = set()


        # -------- Tables --------

        for table in tables:

            rows = []

            for row in table:
                rows.append([it["text"] for it in row])


            blocks.append({
                "type": "table",
                "rows": rows
            })


            for r in table:
                used_lines.add(id(r))


        # -------- Paragraphs --------

        for line in lines:

            if id(line["items"]) in used_lines:
                continue


            text = " ".join(
                it["text"] for it in line["items"]
            )


            if text.strip():

                blocks.append({
                    "type": "paragraph",
                    "text": text
                })


        return {
            "page": ocr_data["image"],
            "blocks": blocks,
            "num_tables": len(tables),
            "num_blocks": len(blocks)
        }


    # --------------------------------------------------
    # Folder
    # --------------------------------------------------

    def analyze_folder(self,
                       input_dir: Path,
                       output_dir: Path):

        output_dir.mkdir(parents=True, exist_ok=True)


        json_files = sorted(input_dir.glob("*.json"))

        print(f"Layout analyze: {len(json_files)} files")


        for jf in json_files:

            with open(jf, "r", encoding="utf-8") as f:
                data = json.load(f)


            analyzed = self.analyze_page(data)


            out_file = output_dir / jf.name


            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(
                    analyzed,
                    f,
                    ensure_ascii=False,
                    indent=2
                )


            print("Analyzed:", jf.name)
