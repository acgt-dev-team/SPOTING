<script setup>
</script>

<template>

<div>

<h1 class="title">Tugasan</h1>

<div class="table">

<div class="row header">
<div>Bil</div>
<div>Nama</div>
<div>Protokol</div>
<div>Julat IP</div>
<div>Peranti</div>
<div>Status</div>
</div>

<div class="row">
<div>1</div>
<div>Tugasan 1</div>
<div>v4</div>
<div>127.0.0.1 - 127.0.0.245</div>
<div class="green">1,233 / 1,233</div>
<div class="status done">Selesai</div>
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
grid-template-columns:60px 1fr 100px 2fr 1fr 120px;
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

.status{
padding:4px 10px;
border-radius:6px;
font-size:12px;
display:inline-block;
}

.done{
background:#dcfce7;
color:#16a34a;
}

</style>