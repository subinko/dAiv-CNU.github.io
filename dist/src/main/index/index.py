from browser import document, window, aio, module_init
print, pyprint = module_init(__name__, "index.index")


########################################################################################################################
# AOS Animation
########################################################################################################################
window.AOS.init()


########################################################################################################################
# Programs List
########################################################################################################################
def enable_isotope():
    programs_container = document.getElementById('programs_container')
    if programs_container:
        window.programs_isotope = window.Isotope.new(programs_container, {
            'itemSelector': ".programs-item",
            'layoutMode': "masonry"
        })
        window.AOS.refresh()


def flag_selected_tag(selected):
    for li in document.getElementById('programs_filter').getElementsByClassName('filter-active'):
        li.classList.remove('filter-active')
    selected.classList.add('filter-active')


def change_filter(event):
    programs_filter = document.getElementById('programs_filter').children
    filter_value = event.currentTarget.dataset.filter
    window.programs_isotope.arrange({'filter': filter_value})
    window.programs_isotope.on('arrangeComplete', lambda _: window.AOS.refresh())
    if 'program-type' in event.currentTarget.classList:
        for fil in programs_filter:
            if filter_value == fil.attributes['data-filter'].nodeValue:
                flag_selected_tag(fil)
                break
    else:
        flag_selected_tag(event.currentTarget)


def setup_programs_filter():
    enable_isotope()
    programs_filter = document.getElementById('programs_filter').children
    for el in programs_filter + list(document.getElementsByClassName('program-type')):
        el.onclick = change_filter


########################################################################################################################
# Set Datas by Year
########################################################################################################################
from common.main import current_year, insert_element

#test_func = lambda e: print(e.target.text)

team = document.getElementById('team')
if team:
    async def add_team_history():
        enabled_years = []
        for year in range(current_year + 1, 2021, -1):
            result = await window.fetch(f"/dist/res/templates/years/{year}/team.html")
            if result.status != 200:
                continue
            insert_element(await result.text(), team.getElementsByClassName("container")[0], -1)
            enabled_years.append(year)

            if len(enabled_years) == 1:
                document.getElementById('team_'+str(year)).style.display = 'block'
                window.AOS.init()
                window.AOS.refresh()

            button = document.createElement("a")
            button.id = f"member_show_button_{year}"
            button.href = "#team"
            button.className = "btn btn-warning rounded-pill scrollto cursor-hover-item"
            button.style.display = "none" if len(enabled_years) > 3 else "block"
            button.style.color = "white"
            button.textContent = str(year)

            button_click_handler = f"""
                document.querySelectorAll('[id^="team_"]').forEach(el => el.style.display = 'none');
                document.getElementById('team_{year}').style.display = 'block'
            """
            button.setAttribute('onclick', button_click_handler)

            document.getElementById('button_container').prepend(button)

    aio.run(add_team_history())


programs = document.getElementById('programs')
if programs:
    async def add_programs_history():
        enabled = False
        for year in range(current_year, 2022, -1):
            result = await window.fetch(f"/dist/res/templates/years/{year}/programs.html")
            if result.status != 200:
                continue
            insert_element(await result.text(), programs.getElementsByClassName("container")[0], -1)
            if not enabled:
                enabled = True
                document.getElementById('programs_'+str(year)).style.display = 'block'
                images = document.select('img')

                for img in images:
                    if not img.complete:
                        images.append(img)
                    await aio.sleep(0.001)

                window.AOS.init()
                window.AOS.refresh()
                setup_programs_filter()

    aio.run(add_programs_history())
