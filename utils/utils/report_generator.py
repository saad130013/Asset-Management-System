from tabulate import tabulate

def generate_styled_report(data, output_type, filename):
    """توليد تقرير ملون بتنسيقات متعددة (للتوسعة مستقبلاً)"""
    if output_type == 'console':
        print(tabulate(data, headers='keys', tablefmt='pretty'))

    elif output_type == 'excel':
        data.to_excel(f"{filename}.xlsx", index=False)

    elif output_type == 'json':
        data.to_json(f"{filename}.json", orient='records', force_ascii=False)
