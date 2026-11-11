const list=document.querySelector('.transport-list'),template=document.querySelector('#transport-template');
document.querySelector('.add-row')?.addEventListener('click',()=>list.append(template.content.cloneNode(true)));
list?.addEventListener('click',e=>{if(e.target.closest('.remove-row')){const rows=list.querySelectorAll('.transport-row');if(rows.length>1)e.target.closest('.transport-row').remove();else e.target.closest('.transport-row').querySelectorAll('input,select').forEach(x=>x.value='')}});
