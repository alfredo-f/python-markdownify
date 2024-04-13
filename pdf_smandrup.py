import PyPDF2


def delete_ranges(
    input_path,
    output_path,
    ranges_to_keep = None,
    ranges_to_delete = None,
):
    ranges_to_keep = ranges_to_keep or []
    ranges_to_delete = ranges_to_delete or []

    # Open the existing PDF
    reader = PyPDF2.PdfReader(input_path)
    writer = PyPDF2.PdfWriter()

    # Calculate the total number of pages
    num_pages = len(reader.pages)

    # ...

    # Write out the new PDF
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)


def main():
    delete_ranges(
        input_path=r"C:\Users\a.fomitchenko\AWS documentation\raw\AWS CloudWatch.pdf",
        output_path=r"C:\Users\a.fomitchenko\AWS documentation\AWS CloudWatch - Agent.pdf",
        ranges_to_keep=[(137, 326), (1733, 1951)],
    )


if __name__ == '__main__':
    main()
