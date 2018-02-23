---
title: Sistem Submisi Formulir Cipta Media Ekspresi
date: 2018-02-23 21:00:00 +07:00
categories:
- Tutorial
tags:
- JAMStack
- GitLab
- Netlify
- Webtask
author: blazeu
comments: true
img: "/uploads/submisi-cipta-media.png"
layout: post
---

![submisi](/uploads/submisi-cipta-media.png){: .img-responsive .center-block }

Pada hibah Cipta Media Ekspresi ini, kontribusi teknologi dikerjakan oleh PT Wahana Medium Cendekia. PT Wahana Medium Cendekia, yang diwakilkan oleh John Mark Vandenberg sebagai spesialis teknologi dan saya sebagai pendampingnya, memutuskan untuk menggunakan [GitLab](https://gitlab.com/) dengan memanfaatkan fitur [_Merge Request_](https://docs.gitlab.com/ee/user/project/merge_requests/index.html) sebagai tempat untuk menaruh permohonan hibah yang datang dari formulir daring. Karena [Sumber kode](https://gitlab.com/ciptamedia/ciptamedia.gitlab.io) situs kami sudah ada di GitLab, memanfaatkan layanan yang sama untuk memproses permohonan hibah merupakan hal logis yang menjadi pilihan.

Situs Cipta Media tidak memiliki _server_ atau _database_ atau bisa disebut [JAMStack](https://jamstack.org/). Semua data permohonan hibah disimpan didalam _file_ biasa menggunakan format [_markdown_](https://id.wikipedia.org/wiki/Markdown) dan siapapun bisa melihatnya didalam [sumber kode](https://gitlab.com/ciptamedia/ciptamedia.gitlab.io/tree/master/_hibahcme) maupun didalam [situs](https://www.ciptamedia.org/ciptamediaekspresi/pemohon-ekspresi.html) Cipta Media. Kami pikir keterbukaan adalah hal yang sangat penting.

Cara kerja formulir daring Cipta Media menjadi sangat sederhana, karena data dari permohonan hibah hanya disimpan pada _file_ biasa. Disinilah peran _Merge Request_ menjadi sangat sejalan. _Merge Request_ berguna untuk membuat sebuah permintaan untuk merubah sumber kode atau _file_ pada situs kami. Satu permohonan menjadi satu _file_ baru di situs kami, dan _file_ tersebut dibuat menggunakan _Merge Request_. Daftar _Merge Request_ untuk setiap permintaan hibah bisa dilihat di [halaman _Merge Request_](https://gitlab.com/ciptamedia/ciptamedia.gitlab.io/merge_requests) _repository_ GitLab kami.

Sesuai dengan namanya, _Merge Request_ hanyalah sebuah permintaan. Permohonan hibah yang dibuat dengan sembarangan tidak akan masuk kedalam sumber kode kami dan halaman daftar pemohon, karena kami melakukan penyaringan terlebih dahulu.

Kami memilih menggunakan [Netlify](https://www.netlify.com/) untuk melayani situs Cipta Media. Netlify menyediakan fitur formulir yang bisa digunakan tanpa harus mengimplementasikan _server_ atau _database_ sendiri dan hasil formulir tersebut juga bisa dikirim ke beberapa integrasi yang tersedia seperti Email, [Slack](https://slack.com/) maupun servis milik sendiri.

Kami membutuhkan suatu servis untuk membuat _Merge Request_ dari setiap submisi formulir yang datang. Oleh karena itu, saya menciptakan [_gitlab-submission_](https://gitlab.com/ciptamedia/JAM/gitlab-submission) sebagai jembatan antara formulir Netlify dan _Merge Request_ GitLab. Program kecil ini ditaruh di [Webtask](https://webtask.io/) sehingga kami tidak perlu khawatir dengan mengurus _server_ sendiri, karena semua itu sudah ditangani oleh Webtask.

Saya tutup blog tutorial ini dengan menyimpulkan tiga hal yang menjadi latar belakang situs Cipta Media Ekspresi, penggunaan GitLab sebagai penyimpanan sumber kode dan data pemohon hibah, Netlify untuk melayani situs kami, dan _gitlab-submission_ sebagai alat untuk membuat _Merge Request_ dari submisi formulir. Jika tertarik pembahasan yang lebih teknis, saya menulis [artikel di blog pribadi saya](https://surya.works/netlify-form-gitlab) mengenai hal ini.
