# MAAS update instructions

## Part 1 - update the app and the dataset

1. Go to your MAAS folder and **copy the folder location** (highlighted in blue in the pic below) by clicking `Ctrl+C`.
<br>
    <img src="https://github.com/AlxndrMlk/maas/raw/main/docs/folder_location.png" width="500">


2. Open **Anaconda Prompt** (just type `anaconda` in your Windows search and it should appear).
<br>
    <img src="https://github.com/AlxndrMlk/maas/raw/main/docs/anaconda_prompt.png" width="500">

3. In your **Anaconda Prompt** type `cd ` (note that there's a space after `cd`) and then paste your folder location by clicking `Ctrl+V`.
<br>
    <img src="https://github.com/AlxndrMlk/maas/raw/main/docs/anaconda_prompt_2.png" width="500">

4. Now you should see your **MAAS folder location** on the left of your cursor. If that's the case, continue 👍🏼

5. Now type `update` in your **Anaconda Prompt**. It should start updating your app.

6. If the previous step has finished successfully, now type `refresh_data` in your **Anaconda Prompt**. The app should start downloading the data and update your database with the new joined dataset.

7. **Congrats!** We're done! 🎉 If you haven't downloaded the new set of PDFs yet, continue to the part 2. 

<br>

## Part 2 - download PDFs (optional)

1. Download PDFs from here: https://cbu-pdf.s3.us-east-2.amazonaws.com/pdf-prqst/pdf_proq.zip (45GB). Save the file in `pdf-library` folder (it's inside your `maas` folder). If you don't have enough space on your main drive, go directly to **Part 3**.

2. Unzip the files directly to the folder (options like `Extract Here` or `Wypakuj tutaj`).

3. After extracting, you can **delete** the zip file (`pdf.zip`).

3. **That's all!** 🎉 Now you can type `maas` in your **Anaconda Prompt** and start using the app with updated PDFs. 

<br>

## Part 3 - download PDFs to another location (optional)

1. Download PDFs from here: https://cbu-pdf.s3.us-east-2.amazonaws.com/pdf-prqst/pdf_proq.zip (45GB). Save the file in any convenient location. 

2. Unzip the files in your folder of choice. After extracting, you can **delete** the zip file (`pdf_proq.zip`).

3. **Importnat**: Copy or move your old PDFs to the same folder.

4. Now copy the folder location.
<br>
    <img src="https://github.com/AlxndrMlk/maas/raw/main/docs/folder_location.png" width="500">

5. Go to your `maas` folder. You should see another folder there called `app-data`. Inside `app-data` there's a file called `pdf-path.dat`.

6. Open `pdf-path.dat` with **Notepad** and overwrite its content. You can do it by selecting all (`Ctrl+A`) and pasting your PDF folder location (`Ctrl+V`). After pasting your folder location save the file (`Ctrl+S`).

7. **That's all!** 🎉 Now you can type `maas` in your **Anaconda Prompt** and start using the app with updated PDFs. 