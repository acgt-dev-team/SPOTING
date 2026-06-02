<script setup>
defineProps({
  modelValue: String,
  label: String,
  placeholder: String,
  type: {
    type: String,
    default: "text"
  }
})

const emit = defineEmits(["update:modelValue"])
</script>

<template>
  <div class="field">
    <label v-if="label" class="label">
      {{ label }}
    </label>

    <input
      :type="type"
      :placeholder="placeholder"
      :value="modelValue"
      @input="emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>

<style scoped>
.field{
  display:flex;
  flex-direction:column;
  gap:8px;
  width:100%;
  margin-bottom:14px;
}

.label{
  font-size:14px;
  font-weight:600;
  color:#334155;
}

input{
  width:100%;
  height:48px;
  padding:0 16px;

  border:1px solid #E2E8F0;
  border-radius:14px;

  background:#F8FAFC;

  font-size:14px;
  color:#0F172A;

  transition:.18s ease;
  box-sizing:border-box;
}

input::placeholder{
  color:#94A3B8;
}

input:hover{
  border-color:#CBD5E1;
}

input:focus{
  outline:none;
  border-color:#4F46E5;
  background:white;
  color:#0F172A;
  box-shadow:0 0 0 3px rgba(79,70,229,.08);
}
</style>