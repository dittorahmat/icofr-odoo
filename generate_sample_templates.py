import pandas as pd

# 1. Generate Sample FSLI Template (Mapping)
fsli_data = {
    'Kode Entity': ['0101', '0101', '0101', '0101', '0101', '114', '114'],
    'Kode BSPL': ['BS', 'BS', 'BS', 'PL', 'PL', 'BS', 'PL'],
    'Kategori': ['Neraca', 'Neraca', 'Neraca', 'Laba Rugi', 'Laba Rugi', 'Neraca', 'Laba Rugi'],
    'Sub Kategori': ['Aset', 'Aset', 'Kewajiban', 'Pendapatan', 'Beban', 'Aset', 'Pendapatan'],
    'Kode FSLI': [
        '01.01.00.00', '01.02.00.00', '02.01.00.00', 
        '04.01.00.00', '05.01.00.00', '01.01.00.00', '04.01.00.00'
    ],
    'Deskripsi FSLI': [
        'Kas dan Setara Kas', 'Piutang Usaha', 'Utang Usaha',
        'Pendapatan Operasional', 'Beban Gaji', 'Kas dan Setara Kas (Anak)', 'Pendapatan (Anak)'
    ]
}

df_fsli = pd.DataFrame(fsli_data)
df_fsli.to_excel('sample_fsli_template.xlsx', index=False)

# 2. Generate Sample General Ledger (Balances)
gl_data = {
    'Kode_Entity': ['0101', '0101', '0101', '0101', '114', '114'],
    'No_GL': ['10001', '10002', '20001', '40001', '10001', '40001'],
    'GL_Desc': [
        'Kas Kecil Kantor Pusat', 'Bank Mandiri - Ops', 
        'Utang Vendor Pihak Ketiga', 'Penjualan Produk A',
        'Kas Kecil Cabang', 'Pendapatan Jasa'
    ],
    'GL_Balance': [
        50000000.0, 1450000000.0, 800000000.0, 
        3500000000.0, 20000000.0, 500000000.0
    ],
    'Kode_FSLI': [
        '01.01.00.00', '01.01.00.00', '02.01.00.00', 
        '04.01.00.00', '01.01.00.00', '04.01.00.00'
    ]
}

df_gl = pd.DataFrame(gl_data)
df_gl.to_excel('sample_general_ledger.xlsx', index=False)

print("Sample files 'sample_fsli_template.xlsx' and 'sample_general_ledger.xlsx' generated successfully.")
