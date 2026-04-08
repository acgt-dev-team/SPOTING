<script setup>
</script>

<template>

<div>

<h1 class="title">Tetapan</h1>

<div class="panel">

<div class="menu">
<div>Profil</div>
<div>Ubah kata laluan</div>
<div>Ubah organisasi</div>
<div class="active">Jenis tugasan</div>
</div>

<div class="content">

<div class="row header">
<div>No</div>
<div>Nama</div>
</div>

<div class="row">
<div>1</div>
<div>Windows client</div>
</div>

<div class="row">
<div>2</div>
<div>Mac client</div>
</div>

</div>

</div>

</div>

</template>

<style scoped>

.title{
font-size:26px;
margin-bottom:20px;
}

.panel{
display:flex;
background:white;
border-radius:12px;
padding:30px;
}

.menu{
width:200px;
border-right:1px solid #eee;
padding-right:20px;
}

.menu div{
margin-bottom:14px;
cursor:pointer;
}

.active{
color:#7c3aed;
font-weight:600;
}

.content{
flex:1;
padding-left:30px;
}

.row{
display:grid;
grid-template-columns:80px 1fr;
padding:12px 0;
border-bottom:1px solid #eee;
}

.header{
font-weight:600;
}

</style>