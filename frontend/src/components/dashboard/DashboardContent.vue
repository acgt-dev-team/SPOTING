<script setup>
</script>

<template>

<div>

<h1 class="title">Gambaran keseluhan</h1>

<div class="cards">

<div class="card">
<div class="number blue">43</div>
<div class="label">Jumlah organisasi</div>
</div>

<div class="card">
<div class="number blue">43</div>
<div class="label">Jumlah organisasi</div>
</div>

<div class="card">
<div class="number green">2.4k <span>/ 10.2k</span></div>
<div class="label">Jumlah tugasan</div>
</div>

<div class="card">
<div class="number green">9.4k</div>
<div class="label">Jumlah peranti selesai</div>
</div>

</div>


<h2 class="section-title">Organisasi</h2>

<div class="table">

<div class="row header">
<div>Bil</div>
<div>Nama</div>
<div>Tugasan</div>
</div>

<div class="row">
<div>1</div>
<div>Kementerian Dalam Negeri</div>
<div class="green">1,233 / 9,000</div>
</div>

</div>

</div>

</template>

<style scoped>

.title{
font-size:28px;
margin-bottom:30px;
}

.cards{
display:grid;
grid-template-columns:repeat(4,1fr);
gap:20px;
margin-bottom:40px;
}

.card{
background:white;
padding:24px;
border-radius:14px;
box-shadow:0 2px 10px rgba(0,0,0,0.04);
}

.number{
font-size:36px;
font-weight:700;
}

.number span{
font-size:14px;
color:#6b7280;
}

.blue{
color:#3b82f6;
}

.green{
color:#22c55e;
}

.label{
margin-top:6px;
font-size:14px;
color:#6b7280;
}

.section-title{
font-size:24px;
margin-bottom:20px;
}

.table{
background:white;
border-radius:14px;
overflow:hidden;
}

.row{
display:grid;
grid-template-columns:80px 1fr 200px;
padding:16px 20px;
border-bottom:1px solid #eee;
}

.header{
font-weight:600;
background:#f8fafc;
}

</style>