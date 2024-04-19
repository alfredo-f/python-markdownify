import PyPDF2


def filter_pdf_file(
    input_path,
    output_path,
    ranges_to_keep = None,
    ranges_to_delete = None,
):
    assert (ranges_to_keep is not None) != (ranges_to_delete is not None)

    # Open the existing PDF
    reader = PyPDF2.PdfReader(input_path)
    writer = PyPDF2.PdfWriter()

    # Calculate the total number of pages
    num_pages = len(reader.pages)

    # Iterate through all pages
    for page_num in range(num_pages):
        if ranges_to_keep is not None:
            # Check if the page is in the range to keep
            if any(
                start <= page_num + 1 <= end
                for start, end in ranges_to_keep
            ):
                writer.add_page(reader.pages[page_num])

        elif ranges_to_delete is not None:
            # Check if the page is in the range to delete
            if not any(
                start <= page_num + 1 <= end
                for start, end in ranges_to_delete
            ):
                writer.add_page(reader.pages[page_num])

        else:
            raise ValueError(ranges_to_keep, ranges_to_delete)

    # Write out the new PDF
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)


def main():
    # AWS Control Tower
    # ranges_to_delete=[
    #             (3, 32),  # Table of contents
    #             (425, 2324),
    #             (2541, 8208),
    #         ],

    # API Gateway
    # ranges_to_delete=[
    #   # Working with REST APIs


    filter_pdf_file(
        input_path=r"C:\Users\a.fomitchenko\AWS documentation\raw\AWS Control Tower - all.pdf",
        output_path=r"C:\Users\a.fomitchenko\AWS documentation\AWS Control Tower.pdf",
        # ranges_to_keep=[(1, 2540)],
        ranges_to_delete=[
            (3, 32),  # Table of contents
            (425, 2324),
            (2541, 8208),
        ],
    )


if __name__ == '__main__':
    main()
