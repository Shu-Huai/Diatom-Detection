<template>
    <div class="content">
        <transition name="move" mode="out-in">
        <router-view > 
        </router-view>
        </transition>
    </div>
</template>

<script>
import'animate.css';
export default {
    name:'Right',
    
}
</script>

<style>

</style>