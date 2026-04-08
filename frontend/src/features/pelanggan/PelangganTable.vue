<script setup>
</script>

<template>

<div>

<h1 class="title">Pengurusan Pengguna</h1>

<div class="table">

<div class="row header">
<div>Bil</div>
<div>Nama</div>
<div>Nama pengguna</div>
<div>Peranan</div>
<div>Email</div>
</div>

<div class="row">
<div>1</div>
<div>Khairul Izwan</div>
<div>khairulizwan</div>
<div>Pentadbir</div>
<div>khairul.izwan@kkm.com.my</div>
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
grid-template-columns:60px 1fr 1fr 1fr 1fr;
padding:16px;
border-bottom:1px solid #eee;
}

.header{
font-weight:600;
background:#f8fafc;
}

</style>