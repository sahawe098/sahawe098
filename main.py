# Nama : Andhika M Rizky 
# NIM : 12220052 

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image

df = pd.read_csv('produksi_minyak_mentah.csv')
df_js = pd.read_json('kode_negara_lengkap.json')

#Kode untuk menghapus organisasi
arr = []
for i in list(df['kode_negara']) :
    if i not in list(df_js['alpha-3']) :
        arr.append(i)
for i in arr :
    df = df[df.kode_negara != i]
    
nation_name = df_js['name']

#sort year
df.sort_values(by=['kode_negara'], inplace=True)
df.reset_index(drop=True, inplace=True)
sum_produksi = [[0, 0] for i in range(len(df.kode_negara.unique()))]
uniq = df.kode_negara.unique()
for i in range(len(sum_produksi)) :
    sum_produksi[i][0] = uniq[i]
j = 0
for i in range(len(df)) :
    if(sum_produksi[j][0] == df['kode_negara'][i]) :
        sum_produksi[j][1] += df['produksi'][i]
    else :
        j += 1
        sum_produksi[j][1] += df['produksi'][i]
sum_produksi = pd.DataFrame(sum_produksi, columns=['kode_negara','total_produksi'])
sum_produksi.sort_values(by=['total_produksi'], ascending=False, inplace=True)
sum_produksi.reset_index(drop=True, inplace=True)
    
col1, col2 = st.columns(2)
soal1a = st.container()
soal1b = st.container()
soal1c = st.container()
soal1d = st.container()
with col1 :

    st.markdown("<h1 style='text-align: left; color: red;'> Data Base Produksi Minyak Mentah </h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: left; color: red;'> Andhika M Rizky </h2>", unsafe_allow_html=True)
    image = Image.open('images.jpg')
    st.image(image, width=200)

#1a
    with soal1a:
        st.markdown("<h2 style='text-align: left; color: red;'> Grafik jumlah produksi minyak mentah </h2>", unsafe_allow_html=True)
        option = st.selectbox(
            "",
            nation_name
        )
        choosen_nation = df_js.loc[df_js['name'] == option]
        choosen_nation.reset_index(drop=True, inplace=True)
        nation_code = str(choosen_nation['alpha-3'][0])
        result1 = df.loc[df['kode_negara'] == nation_code]
        result1 = result1[['tahun', 'produksi']]
        result1.reset_index(drop=True, inplace=True)
        #menampilkan grafik
        chart = alt.Chart(result1).mark_line().encode(
            x='tahun',
            y='produksi'
        )
        st.altair_chart(chart, use_container_width=True)
            
 #1b
    with soal1b :
        st.markdown("<h2 style='text-align: left; color: red;'> Peringkat Negara Dengan Jumlah Produksi Terbesar Pada Tahun Tertentu </h2>", unsafe_allow_html=True)
        df1 = pd.read_json("kode_negara_lengkap.json")
        df2 = pd.read_csv("produksi_minyak_mentah.csv")
        df = pd.merge(df2,df1,left_on='kode_negara',right_on='alpha-3')

        list_negara = df["name"].unique().tolist()
        list_negara.sort()
        jumlah_negara = st.selectbox("Pilih negara", range(1, len(list_negara)), 9)
        tahun = st.selectbox("Pilih tahun", range(1971, 2016), 44)

        st.subheader(f'{jumlah_negara} besar negara dengan jumlah produksi terbesar pada tahun {tahun}')

        res = df[(df.tahun == tahun)][["name", "produksi"]].sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
        res.index += 1

        source = res.iloc[:jumlah_negara]
        
        #making graph with altair
        bars = alt.Chart(source).mark_bar().encode(
            x='produksi',
            y=alt.Y(
                    "name",
                    sort=alt.EncodingSortField(field="produksi", order="descending"),
                    title="Negara"))

        text = bars.mark_text(
            align='left',
            baseline='middle',
            color='black',
            dx=3 
        ).encode(
            text='produksi'
        )
        chart = (bars).configure_view(
        strokeWidth=10
    )
        
        st.altair_chart(chart, use_container_width=True)

    #1c
    with soal1c :
        st.markdown("<h2 style='text-align: left; color: red;'> Peringkat Negara Dengan Jumlah Produksi Terbesar Keseluruhan </h2>", unsafe_allow_html=True)
        #menerima masukan jumlah negara
        nation_count = int(st.number_input('Masukkan jumlah negara yang ingin ditampilkan'))
        #Knegara-negara yang memiliki jumlah kumulatif terbesar
        if(len(sum_produksi) >= nation_count) :
            result3 = sum_produksi.head(nation_count)
        result3
        #Kode untuk menampilkan grafik 
        bars2 = alt.Chart(result3).mark_bar().encode(
            x='kode_negara',
            y='total_produksi'
        )
        st.altair_chart(bars2, use_container_width=True)


    #1d
    with soal1d :
        st.markdown("<h2 style='text-align: left; color: red;'> Informasi Produksi </h2>", unsafe_allow_html=True)
        df = pd.read_csv('produksi_minyak_mentah.csv')
        df_js = pd.read_json('kode_negara_lengkap.json')

        df_year = df.loc[df['tahun'] == tahun]
        df_year.sort_values(by=['produksi'], ascending=False, inplace=True)
        df_year.reset_index(drop=True, inplace=True)
        df2 = df
        df2.sort_values(by=['produksi'], ascending=False, inplace=True)
        df2.reset_index(drop=True, inplace=True)
        if 1==1:
            if(len(df_year) > 0) :
                #Kode untuk menampilkan informasi nama lengkap negara, kode negara, region, dan sub-region dengan jumlah produksi terbesar pada tahun T dan keseluruhan tahun
                max_nat = df_year.head(1)
                max_nat_code = str(max_nat["kode_negara"][0])
                nat_info = df_js.loc[df_js['alpha-3'] == max_nat_code]
                nat_info.reset_index(drop=True, inplace=True)
                st.write("Informasi negara dengan jumlah produksi terbesar pada tahun", str(tahun))
                if(len(nat_info) > 0) :
                    res = [[str(nat_info['name'][0]), str(max_nat_code), str(nat_info['region'][0]), str(nat_info['sub-region'][0])]]
                    res = pd.DataFrame(res, columns=['Nama negara', 'Kode negara', 'Region ', 'Sub-region'])
                    res
                else :
                    st.write("Informasi negara kurang lengkap selain kode negara")
                    st.write("Kode negara : ", str(max_nat_code))
                max_nat_all_year = df2.head(1)
                max_nat_all_year_code = str(max_nat_all_year["kode_negara"][0])
                nat_all_year_info = df_js.loc[df_js['alpha-3'] == max_nat_all_year_code]
                nat_all_year_info.reset_index(drop=True, inplace=True)
                st.write("Informasi negara dengan jumlah produksi terbesar keseluruhan tahun")
                if(len(nat_all_year_info) > 0) :
                    res2 = [[str(nat_all_year_info['name'][0]), str(max_nat_all_year_code), str(nat_all_year_info['region'][0]), str(nat_all_year_info['sub-region'][0])]]
                    res2 = pd.DataFrame(res2, columns=['Nama negara', 'Kode negara', 'Region ', 'Sub-region'])
                    res2
                else :
                    st.write("Informasi negara kurang lengkap selain kode negara")
                    st.write("Kode negara : ", str(max_nat_all_year_code))
        if 1==1:
            #Kode untuk menampilkan informasi nama lengkap negara, kode negara, region, dan sub-region dengan jumlah produksi terkecil (tidak sama dengan nol) pada tahun T dan keseluruhan tahun
            df2 = df.loc[df['produksi'] > 0]
            df2.sort_values(by=['produksi'], inplace=True)
            df2.reset_index(drop=True, inplace=True)
            df_year = df2.loc[df2['tahun'] == tahun]
            df_year.sort_values(by=['produksi'], inplace=True)
            df_year.reset_index(drop=True, inplace=True)
            if(len(df_year) > 0) :
                min_nat = df_year.head(1)
                min_nat_code = str(min_nat["kode_negara"][0])
                nat_info = df_js.loc[df_js['alpha-3'] == min_nat_code]
                nat_info.reset_index(drop=True, inplace=True)
                st.write("Informasi negara dengan jumlah produksi terkecil pada tahun", str(tahun))
                if(len(nat_info) > 0) :
                    res = [[str(nat_info['name'][0]), str(min_nat_code), str(nat_info['region'][0]), str(nat_info['sub-region'][0])]]
                    res = pd.DataFrame(res, columns=['Nama negara', 'Kode negara', 'Region ', 'Sub-region'])
                    res
                else :
                    st.write("Informasi negara kurang lengkap selain kode negara")
                    st.write("Kode negara : ", str(min_nat_code))
                min_nat_all_year = df2.head(1)
                min_nat_all_year_code = str(min_nat_all_year["kode_negara"][0])
                nat_all_year_info = df_js.loc[df_js['alpha-3'] == min_nat_all_year_code]
                nat_all_year_info.reset_index(drop=True, inplace=True)
                st.write("Informasi negara dengan jumlah produksi terkecil keseluruhan tahun")
                if(len(nat_all_year_info) > 0) :
                    res2 = [[str(nat_all_year_info['name'][0]), str(min_nat_all_year_code), str(nat_all_year_info['region'][0]), str(nat_all_year_info['sub-region'][0])]]
                    res2 = pd.DataFrame(res2, columns=['Nama negara', 'Kode negara', 'Region ', 'Sub-region'])
                    res2
                else :
                    st.write("Informasi negara kurang lengkap selain kode negara")
                    st.write("Kode negara : ", str(min_nat_all_year_code))

        if 1==1:
            #Kode untuk menampilkan informasi nama lengkap negara, kode negara, region, dan sub-region dengan jumlah produksi sama dengan nol pada tahun T dan keseluruhan tahun
            df2 = df.loc[df['produksi'] == 0]
            df2.sort_values(by=['kode_negara'], inplace=True)
            df2.reset_index(drop=True, inplace=True)
            df2_uniq = df2.kode_negara.unique()
            df_year = df2.loc[df2['tahun'] == tahun]
            df_year.sort_values(by=['kode_negara'], inplace=True)
            df_year.reset_index(drop=True, inplace=True)
            df_year_uniq = df_year.kode_negara.unique()
            if(len(df_year) > 0) :
                res = [[0, 0, 0, 0] for i in range(len(df_year_uniq))]
                for i in range(len(res)) :
                    code = str(df_year_uniq[i])
                    nat_info = df_js.loc[df_js['alpha-3'] == code]
                    nat_info.reset_index(drop=True, inplace=True)
                    res[i][0] = str(nat_info['name'][0])
                    res[i][1] = str(df_year_uniq[i])
                    res[i][2] = str(nat_info['region'][0])
                    res[i][3] = str(nat_info['sub-region'][0])
                st.write("Informasi negara dengan jumlah produksi nol pada tahun ", str(tahun))
                res = pd.DataFrame(res, columns=['Nama negara', 'Kode negara', 'Region ', 'Sub-region'])
                res
                res2 = [[0, 0, 0, 0] for i in range(len(df2_uniq))]
                for i in range(len(res2)) :
                    code = str(df2_uniq[i])
                    nat_info = df_js.loc[df_js['alpha-3'] == code]
                    nat_info.reset_index(drop=True, inplace=True)
                    res2[i][0] = str(nat_info['name'][0])
                    res2[i][1] = str(df2_uniq[i])
                    res2[i][2] = str(nat_info['region'][0])
                    res2[i][3] = str(nat_info['sub-region'][0])
                st.write("Informasi negara dengan jumlah produksi nol pada seluruh tahun ")
                res2 = pd.DataFrame(res2, columns=['Nama negara', 'Kode negara', 'Region ', 'Sub-region'])
                res2
