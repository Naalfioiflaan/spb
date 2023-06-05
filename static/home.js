const data = document.currentScript.dataset
const rp_tgl_terakhir_diambil = data.rpTgl
const hr_tgl_terakhir_diambil = data.hrTgl
console.log(rp_tgl_terakhir_diambil)

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
const rp_tgl_awal = rp_tgl_default.toISOString().substring(0, 10);
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
const hr_tgl_awal = hr_tgl_default.toISOString().substring(0, 10);
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