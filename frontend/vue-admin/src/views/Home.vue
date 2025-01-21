
<template>
  <div>
    <Header />
    <Sidebar />
    <div class="content-box" :class="tt">
      <Right/>
    </div>
    
  </div>
</template>

<script>
import Header from "@/components/Header";
import Sidebar from "@/components/Sidebar";
import Right from '@/components/Right';
export default {
  name: "Home",
  components: { Header, Sidebar,Right },
  data(){
        return{
            tt:''
        }
    },
    created(){
        this.$bus.$on('tt',(data)=>{
            if(data){
               this.tt='content-collapse'
            }else{
                this.tt=''
            }
        })  
    },
    mounted() {
      console.log("Home component mounted");
    },
};
</script>

<style>
</style>