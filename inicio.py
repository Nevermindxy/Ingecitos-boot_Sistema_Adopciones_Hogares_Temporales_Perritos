from tkinter import ttk

class Inicio:
    def __init__(self,parent,db):
        self.db=db
        ttk.Label(parent,text='Panel general · Huellitas',style='Titulo.TLabel').pack(pady=20)
        panel=ttk.Frame(parent); panel.pack(fill='x',padx=20)
        self.labels=[]
        for i,t in enumerate(['Total de perritos','Disponibles','Hogar temporal','Adoptados','Cupos libres','Estadías vencidas']):
            card=ttk.LabelFrame(panel,text=t,padding=15); card.grid(row=i//3,column=i%3,sticky='nsew',padx=6,pady=6)
            panel.columnconfigure(i%3,weight=1)
            label=ttk.Label(card,text='—',style='Titulo.TLabel'); label.pack(); self.labels.append(label)
        ttk.Label(parent,text='Las estadías vencidas requieren confirmar el retorno real del perro.').pack(pady=15)
        ttk.Button(parent,text='Actualizar',command=self.cargar_datos).pack()
        self.cargar_datos()
    def cargar_datos(self):
        consultas=['SELECT COUNT(*) FROM perro',*["SELECT COUNT(*) FROM perro WHERE estado='"+s+"'" for s in ['Disponible','Hogar Temporal','Adoptado']], 'SELECT COALESCE(SUM(GREATEST(h.capacidad-(SELECT COUNT(*) FROM asignacion_temporal a WHERE a.id_hogar=h.id_hogar AND a.finalizada=0),0)),0) FROM hogar_temporal h','SELECT COUNT(*) FROM asignacion_temporal WHERE finalizada=0 AND fecha_fin<CURDATE()']
        for label,sql in zip(self.labels,consultas):
            c=self.db.ejecutar(sql); label.config(text=str(c.fetchone()[0]) if c else '—')
