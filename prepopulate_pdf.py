"""
Example script illustrating how to programmatically fill out a pdf.

Particularly helpful in cases when the user needs to fill out a number of pdfs
with well defined information instead of conducting manual data entry.

To apply this to your usecase, you will need to:
  1. determine the fields of the pdf using reader.get_fields()
"""

import pypdf as p


def create_filled_pdf(template_pdf, name_value, output_path="output/filled.pdf", print_fields=False):
    """
    Args:
      name_value: Dict[str, str], Field Name mapped to requested value.
      output_path: Path where the output, filled pdf will be saved.
      print_fields: If set to true, will print all text field forms within the pdf, helpful to determine field_names.
    """

    if not name_value:
        print("User provided empty name_value argument exiting.")
        return

    reader = p.PdfReader(template_pdf)
    writer = p.PdfWriter()
    writer.append(reader)

    # Determine the fields which must be filled.
    fields = reader.get_fields()
    for key, value in fields.items():
        field_name = value.get("/T", None)
        field_type = value.get("/FT", None)
        if print_fields and field_type == "/Tx":
            print(
                f"Field Name to use: {field_name}, Current value: {value.get('/V','')}"
            )

        if field_name in name_value:
            if print_fields:
                print(f"Updating: {field_name} with Value: {name_value[field_name]}")
            page_substring_loc = key.lower().find("page")

            if page_substring_loc != -1:
                # We index starting at 0 btw.
                page_number = int(key[page_substring_loc + 4]) - 1
            else:
                page_number = 0

            writer.update_page_form_field_values(
                writer.pages[page_number], {field_name: name_value[field_name]}
            )

    with open(output_path, "wb") as out_fd:
        writer.write(out_fd)
    print(f"wrote {output_path}")


if __name__ == "__main__":
    TEMPLATE_FILE = "fillable/t2200-fill-23e.pdf"
    EXAMPLE_ENTRIES = [{
        "Last_Name_Fill[0]": "Mario",
        "First_Name_Fill[0]": "Mario",
        "Tax_Year_Fill[0]": "1969",
        "Business_Address_Fill[0]": "245 Peach Crescent, Mushroom Kingdom",
        "Job_Title_Fill[0]": "Plumber, Head of National Defence",
        "FromDate[0]": "19810101",
        "ToDate[0]": "20231231",
        },
        {
        "Last_Name_Fill[0]": "Luigi",
        "First_Name_Fill[0]": "Mario",
        "Tax_Year_Fill[0]": "1969",
        "Business_Address_Fill[0]": "245 Peach Crescent, Mushroom Kingdom",
        "Job_Title_Fill[0]": "Plumber, Deputy of National Defence, Homeowner",
        "FromDate[0]": "19830101",
        "ToDate[0]": "20231231",
        },
        {
        "Last_Name_Fill[0]": "Peach",
        "First_Name_Fill[0]": "Princess",
        "Tax_Year_Fill[0]": "1969",
        "Business_Address_Fill[0]": "245 Peach Crescent, Mushroom Kingdom",
        "Job_Title_Fill[0]": "Matriarch, Passenger",
        "FromDate[0]": "19850101",
        "ToDate[0]": "20231231",
        },
    ]

    for entry in EXAMPLE_ENTRIES:
        file_name = "_".join(list(entry.values())[:2]).lower()
        create_filled_pdf(TEMPLATE_FILE, entry, f"output/{file_name}.pdf", print_fields=False)
