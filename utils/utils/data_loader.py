import pandas as pd

def load_assets(file_path):
    """تحميل بيانات الأصول من ملف Excel"""
    try:
        df = pd.read_excel(
            file_path,
            engine='openpyxl',
            dtype={
                'GL_account': str,
                'Asset_Code_For_Accounting_Purpose': str
            }
        )

        required_columns = [
            'Asset_Code_For_Accounting_Purpose',
            'GL_account',
            'Cost',
            'City',
            'Useful_Life'
        ]

        if not all(col in df.columns for col in required_columns):
            missing = [col for col in required_columns if col not in df.columns]
            raise ValueError(f"الملف ينقصه الأعمدة التالية: {missing}")

        return df

    except FileNotFoundError:
        raise FileNotFoundError("لم يتم العثور على ملف الأصول المحدد")
