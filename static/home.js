const data = document.currentScript.dataset
let rp_tgl_terakhir_diambil = new Date();
let hr_tgl_terakhir_diambil = new Date();
let gr_tgl_terakhir_diambil = new Date();
let tp_tgl_terakhir_diambil = new Date();
rp_tgl_terakhir_diambil.setDate(rp_tgl_terakhir_diambil.getDate() - 7);
hr_tgl_terakhir_diambil.setDate(hr_tgl_terakhir_diambil.getDate() - 7);
gr_tgl_terakhir_diambil.setDate(gr_tgl_terakhir_diambil.getDate() - 7);
tp_tgl_terakhir_diambil.setDate(tp_tgl_terakhir_diambil.getDate() - 7);
if (data.rpTgl != '') rp_tgl_terakhir_diambil = data.rpTgl
if (data.hrTgl != '') hr_tgl_terakhir_diambil = data.hrTgl
if (data.grTgl != '') gr_tgl_terakhir_diambil = data.grTgl
if (data.tpTgl != '') tp_tgl_terakhir_diambil = data.tpTgl


function showLoading() {
    const loading = document.getElementById('loading');
    loading.classList.remove('d-none');
    console.log('tekan')
}

function getDatesInRange(startDate) {
const date = startDate;
date.setDate(date.getDate()+1)
const dates = [];

const endDate = new Date()
endDate.setHours(0, 0, 0, 0)

while (date < endDate) {
    const tgl = new Date(date)
    dates.push(tgl);
    date.setDate(date.getDate() + 1);
}

return dates;
}

// Riau pos
const rp_tgl_terakhir = new Date(rp_tgl_terakhir_diambil);
const rp_tgl_default = rp_tgl_terakhir;
rp_tgl_default.setDate(rp_tgl_default.getDate() + 1);
const rp_tgl_string = new Date(rp_tgl_default - new Date().getTimezoneOffset() * 60000).toISOString()
const rp_tgl_awal = rp_tgl_string.substring(0, 10);
document.getElementById('rp_tgl_awal').value = rp_tgl_awal
new tempusDominus.TempusDominus(
document.getElementById('riauposDatePicker'),
{
    allowInputToggle: true,
    useCurrent: false,
    defaultDate: rp_tgl_default,
    restrictions: {
    enabledDates: getDatesInRange(new Date(rp_tgl_terakhir_diambil)),
    },
    display: {
    components: {
        clock: false,
    },
    theme: 'light',
    placement: 'top',
    },
    localization: {
    dateFormats: {
        L: 'yyyy-MM-dd',
        LT: 'MMM dd, yyyy'
    },
    format: 'yyyy-MM-dd',
    },
}
);

// Haluan Riau
const hr_tgl_terakhir = new Date(hr_tgl_terakhir_diambil);
const hr_tgl_default = hr_tgl_terakhir;
hr_tgl_default.setDate(hr_tgl_default.getDate() + 1);
const hr_tgl_string = new Date(hr_tgl_default - new Date().getTimezoneOffset() * 60000).toISOString()
const hr_tgl_awal = hr_tgl_string.substring(0, 10);
document.getElementById('hr_tgl_awal').value = hr_tgl_awal
new tempusDominus.TempusDominus(
document.getElementById('haluanriauDatePicker'),
{
    allowInputToggle: true,
    useCurrent: false,
    defaultDate: hr_tgl_default,
    restrictions: {
    enabledDates: getDatesInRange(new Date(hr_tgl_terakhir_diambil)),
    },
    display: {
    components: {
        clock: false,
    },
    theme: 'light',
    placement: 'top',
    },
    localization: {
    dateFormats: {
        L: 'yyyy-MM-dd',
        LT: 'MMM dd, yyyy'
    },
    format: 'yyyy-MM-dd',
    },
}
);

// Go Riau
const gr_tgl_terakhir = new Date(gr_tgl_terakhir_diambil);
const gr_tgl_default = gr_tgl_terakhir;
gr_tgl_default.setDate(gr_tgl_default.getDate() + 1);
const gr_tgl_string = new Date(gr_tgl_default - new Date().getTimezoneOffset() * 60000).toISOString()
const gr_tgl_awal = gr_tgl_string.substring(0, 10);
// console.log(gr_tgl_awal)
document.getElementById('gr_tgl_awal').value = gr_tgl_awal
new tempusDominus.TempusDominus(
document.getElementById('goriauDatePicker'),
{
    allowInputToggle: true,
    useCurrent: false,
    defaultDate: gr_tgl_default,
    restrictions: {
    enabledDates: getDatesInRange(new Date(gr_tgl_terakhir_diambil)),
    },
    display: {
    components: {
        clock: false,
    },
    theme: 'light',
    placement: 'top',
    },
    localization: {
    dateFormats: {
        L: 'yyyy-MM-dd',
        LT: 'MMM dd, yyyy'
    },
    format: 'yyyy-MM-dd',
    },
}
);

// Tribun Pekanbaru
const tp_tgl_terakhir = new Date(tp_tgl_terakhir_diambil);
const tp_tgl_default = tp_tgl_terakhir;
tp_tgl_default.setDate(tp_tgl_default.getDate() + 1);
const tp_tgl_string = new Date(tp_tgl_default - new Date().getTimezoneOffset() * 60000).toISOString()
const tp_tgl_awal = tp_tgl_string.substring(0, 10);
console.log(tp_tgl_awal)
document.getElementById('tp_tgl_awal').value = tp_tgl_awal
new tempusDominus.TempusDominus(
document.getElementById('tribunpekanbaruDatePicker'),
{
    allowInputToggle: true,
    useCurrent: false,
    defaultDate: tp_tgl_default,
    restrictions: {
    enabledDates: getDatesInRange(new Date(tp_tgl_terakhir_diambil)),
    },
    display: {
    components: {
        clock: false,
    },
    theme: 'light',
    placement: 'top',
    },
    localization: {
    dateFormats: {
        L: 'yyyy-MM-dd',
        LT: 'MMM dd, yyyy'
    },
    format: 'yyyy-MM-dd',
    },
}
);