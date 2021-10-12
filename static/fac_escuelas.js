$('#facultad').on('change', function (e) {
    let facultad = e.target.value;
    let escuelas = fac_escuelas[facultad];
    $('#escuela').empty();
    let opciones = '<option value="">-------------------</option>'
    escuelas.map(element => {
        opciones += `<option value="${element.value}">${element.label}</option>`
    });
    $('#escuela').append(opciones);
});


let departamentos = ubigeo.departamentos
let provincias = ubigeo.provincias
let distritos = ubigeo.distritos

$('#departarmento_nacimiento').empty();
$('#departarmento_residencia').empty();

let opciones_departamentos = '<option value="">-------------------</option>'
departamentos.map(element => {
    opciones_departamentos += `<option value="${element.id_ubigeo}">${element.nombre_ubigeo}</option>`
});
$('#departarmento_nacimiento').append(opciones_departamentos);
$('#departarmento_residencia').append(opciones_departamentos);


$('#departarmento_nacimiento').on('change', function(e){
    let departamento_ubigeo = e.target.value;
    let provincias_nacimiento = provincias[departamento_ubigeo];
    $('#provincia_nacimiento').empty();
    let opciones = '<option value="">-------------------</option>'
    provincias_nacimiento.map(element => {
        opciones += `<option value="${element.id_ubigeo}">${element.nombre_ubigeo}</option>`
    });
    $('#provincia_nacimiento').append(opciones);
});

$('#provincia_nacimiento').on('change', function(e){
    let provincia_ubigeo = e.target.value;
    let distrito_provincias = distritos[provincia_ubigeo];
    $('#distrito_nacimiento').empty();
    let opciones = '<option value="">-------------------</option>'
    distrito_provincias.map(element => {
        opciones += `<option value="${element.id_ubigeo}">${element.nombre_ubigeo}</option>`
    });
    $('#distrito_nacimiento').append(opciones);
});

$('#departarmento_residencia').on('change', function(e){
    let departamento_ubigeo = e.target.value;
    let provincias_nacimiento = provincias[departamento_ubigeo];
    $('#provincia_residencia').empty();
    let opciones = '<option value="">-------------------</option>'
    provincias_nacimiento.map(element => {
        opciones += `<option value="${element.id_ubigeo}">${element.nombre_ubigeo}</option>`
    });
    $('#provincia_residencia').append(opciones);
});

$('#provincia_residencia').on('change', function(e){
    let provincia_ubigeo = e.target.value;
    let distrito_provincias = distritos[provincia_ubigeo];
    $('#distrito_residencia').empty();
    let opciones = '<option value="">-------------------</option>'
    distrito_provincias.map(element => {
        opciones += `<option value="${element.id_ubigeo}">${element.nombre_ubigeo}</option>`
    });
    $('#distrito_residencia').append(opciones);
});

$('#nacionalidad').empty();
let opciones_nacionalidad = '<option value="">-------------------</option>'
nacionalidades.map(element => {
    opciones_nacionalidad += `<option value="${element.code}">${element.name}</option>`
});
$('#nacionalidad').append(opciones_nacionalidad);

