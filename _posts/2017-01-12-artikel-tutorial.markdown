---
title: Artikel Tutorial
date: 2017-01-12 16:49:00 +07:00
categories:
- CMS
- Tutorial
tags:
- Tutorial
author: admincmb
comments: true
img: "/uploads/favicon.ico"
---

## Menulis di Siteleaf

*menulis teks miring* atau _menulis teks miring_

**menulis teks tebal** atau __menulis teks tebal__

~~mencoret teks~~

```
*menulis teks miring* atau _menulis teks miring_

**menulis teks tebal** atau __menulis teks tebal__

~~mencoret teks~~
```

---

1. Poin pertama
2. Poin kedua
  * sub poin kedua
  * sub poin kedua
3. Poin ke tiga
   1. sub poin ketiga dengan urutan
   2. sub poin
4. Poin ke empat    
    penjelasan poin ke empat ditulis dengan menggunakan empat kali spasi  
    penjelasan ini dapat ditulis berbaris-baris
5. Poin ke lima

```
1. Poin pertama
2. Poin kedua
  * sub poin kedua
  * sub poin kedua
3. Poin ke tiga
   1. sub poin ketiga dengan urutan
   2. sub poin
4. Poin ke empat    
    penjelasan poin ke empat ditulis dengan menggunakan empat kali spasi  
    penjelasan ini dapat ditulis berbaris-baris
5. Poin ke lima
```

---

Memasukan link dapat ditulis seperti ini: `[Google](https://www.google.com)`

[Google](https://www.google.com)

Contoh gambar: `![favicon.ico](/uploads/favicon.ico "Logo PKT")`

![favicon.ico](/uploads/favicon.ico "Logo PKT")

Gambar responsif: `![favicon.ico](/uploads/favicon.ico "Logo PKT"){: .img-responsive .center-block }`

![favicon.ico](/uploads/favicon.ico "Logo PKT"){: .img-responsive .center-block }

---

Gambar rata kanan: `<img style="float: right;" src="/uploads/favicon.ico">`

<img style="float: right;" src="/uploads/favicon.ico">
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer tincidunt dui ut nisl accumsan tincidunt. Maecenas turpis mi, auctor nec sollicitudin a, euismod id mauris. Quisque laoreet, nisl auctor ornare ultricies, quam lorem pellentesque nisi, et varius elit ligula in arcu. Maecenas dolor metus, placerat in volutpat sed, pharetra id elit. In vel molestie lorem, a fringilla arcu. Nullam consectetur rhoncus urna at interdum. Pellentesque at interdum massa. Praesent sodales nulla sem, id finibus purus convallis eget. Donec auctor nulla sed dolor molestie, quis pulvinar tortor ullamcorper. Praesent id faucibus est, euismod hendrerit diam. Morbi cursus in quam nec aliquet. Cras sit amet scelerisque lacus. Sed tincidunt pellentesque nisi, quis fermentum metus pharetra at. In eget nunc id neque rhoncus scelerisque.

Integer tristique ante arcu, at dignissim tortor tristique et. Integer commodo in neque vel ultricies. Cras ipsum dui, bibendum a ullamcorper ut, tempus id ex. Proin faucibus maximus mauris, consequat feugiat ipsum consequat ut. Etiam ac erat dolor. Maecenas quam nulla, condimentum porttitor eleifend ullamcorper, lacinia non erat. Etiam malesuada auctor dui mattis accumsan. Vestibulum molestie, metus ac facilisis ultricies, lacus nisi porttitor leo, eu euismod risus odio ultrices nibh. Vivamus quis condimentum metus. Nam commodo odio vitae dolor pharetra, sed consequat sapien finibus. Aliquam magna mauris, semper at ex id, gravida blandit lacus. Phasellus risus sem, viverra et dignissim at, dapibus id justo. Nunc rhoncus sit amet libero vel venenatis. Vestibulum eros ex, auctor at neque a, aliquam rhoncus nisi. Duis condimentum leo et turpis fringilla pulvinar. Morbi fermentum sollicitudin turpis, sit amet commodo dolor dictum nec.

---

Gambar rata kiri: `<img style="float: left;" src="/uploads/favicon.ico" class="img-responsive" width="100"> --> atur ukuran gambar dengan mengubah variabel "width"`

<img style="float: left;" src="/uploads/favicon.ico" class="img-responsive" width="100">
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer tincidunt dui ut nisl accumsan tincidunt. Maecenas turpis mi, auctor nec sollicitudin a, euismod id mauris. Quisque laoreet, nisl auctor ornare ultricies, quam lorem pellentesque nisi, et varius elit ligula in arcu. Maecenas dolor metus, placerat in volutpat sed, pharetra id elit. In vel molestie lorem, a fringilla arcu. Nullam consectetur rhoncus urna at interdum. Pellentesque at interdum massa. Praesent sodales nulla sem, id finibus purus convallis eget. Donec auctor nulla sed dolor molestie, quis pulvinar tortor ullamcorper. Praesent id faucibus est, euismod hendrerit diam. Morbi cursus in quam nec aliquet. Cras sit amet scelerisque lacus. Sed tincidunt pellentesque nisi, quis fermentum metus pharetra at. In eget nunc id neque rhoncus scelerisque.

Integer tristique ante arcu, at dignissim tortor tristique et. Integer commodo in neque vel ultricies. Cras ipsum dui, bibendum a ullamcorper ut, tempus id ex. Proin faucibus maximus mauris, consequat feugiat ipsum consequat ut. Etiam ac erat dolor. Maecenas quam nulla, condimentum porttitor eleifend ullamcorper, lacinia non erat. Etiam malesuada auctor dui mattis accumsan. Vestibulum molestie, metus ac facilisis ultricies, lacus nisi porttitor leo, eu euismod risus odio ultrices nibh. Vivamus quis condimentum metus. Nam commodo odio vitae dolor pharetra, sed consequat sapien finibus. Aliquam magna mauris, semper at ex id, gravida blandit lacus. Phasellus risus sem, viverra et dignissim at, dapibus id justo. Nunc rhoncus sit amet libero vel venenatis. Vestibulum eros ex, auctor at neque a, aliquam rhoncus nisi. Duis condimentum leo et turpis fringilla pulvinar. Morbi fermentum sollicitudin turpis, sit amet commodo dolor dictum nec.

---

> menulis quote dengan menambahkan simbol `>` di depan sebuah paragraf. dengan demikian seluruh paragraf akan berubah menjadi quote. untuk mengakhiri sebuah quote, anda cukup menekan `enter` dua kali dan memulai baris baru

---

memasukan video youtube:

Responsif
<div class="embed-responsive embed-responsive-16by9">
<iframe class="embed-responsive-item" src="https://www.youtube.com/embed/hxJ9coOc7XY"></iframe>
</div>

```
<div class="embed-responsive embed-responsive-16by9">
<iframe class="embed-responsive-item" src="https://www.youtube.com/embed/hxJ9coOc7XY"></iframe>
</div>
```

Tidak responsif
<iframe width="560" height="315" src="https://www.youtube.com/embed/hxJ9coOc7XY" frameborder="0" allowfullscreen></iframe>

```
<iframe width="560" height="315" src="https://www.youtube.com/embed/hxJ9coOc7XY" frameborder="0" allowfullscreen></iframe>
```
