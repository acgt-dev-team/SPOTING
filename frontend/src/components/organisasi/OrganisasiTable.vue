<script setup>
</script>

<template>

<div>

<h1 class="title">Organisasi</h1>

<div class="table">

<div class="row header">
<div>Bil</div>
<div>Nama</div>
<div>Sub organisasi</div>
<div>Tapak</div>
<div>Tugasan</div>
</div>

<div class="row">
<div>1</div>
<div>Kementerian Dalam Negeri</div>
<div>200</div>
<div>828</div>
<div class="green">1,233 / 9,000</div>
</div>

</div>

</div>

</template>

<style scoped>

.title{
font-size:26px;
margin-bottom:20px;
}

.table{
background:white;
border-radius:12px;
overflow:hidden;
}

.row{
display:grid;
grid-template-columns:60px 2fr 1fr 1fr 1fr;
padding:16px;
border-bottom:1px solid #eee;
}

.header{
font-weight:600;
background:#f8fafc;
}

.green{
color:#22c55e;
font-weight:600;
}

</style>