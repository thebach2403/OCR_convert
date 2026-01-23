import argparse
# from input.pdf_reader import read_pdf
# from calculator.gum import calculate_uncertainty
# from report.pdf_generator import generate_pdf

def main():
    parser = argparse.ArgumentParser(
        description="Measurement Uncertainty Report Generator"
    )
    parser.add_argument("input", help="Input PDF or Excel file")
    parser.add_argument("--type", required=True, help="Measurement type")
    parser.add_argument("--output", default="output/reports")

    args = parser.parse_args()

    # data = read_pdf(args.input)
    # result = calculate_uncertainty(data, args.type)
    # generate_pdf(result, args.output)

if __name__ == "__main__":
    main()