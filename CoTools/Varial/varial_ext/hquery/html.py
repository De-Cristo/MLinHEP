"""Templates and functions for html."""


msg_reload = '<a href="index.html">reload</a> (automatic every 3 seconds)'

section_form = """\
<form method="post" accept-charset="ASCII" autocomplete="off">
  <input type="text" name="create section" value="new_section" required=true>
  <input type="submit" value="{button}">
</form>
"""

delete_form = """\
<form method="post" action="{action_dir}index.html" \
      onsubmit="return confirm('Really {value}?');">
  <input type="submit" name="delete" value="{value}" style="color:#f00;">
  <input type="hidden" name="{value}" value={name}>
</form>
"""

histo_form = """\
<form method="post" accept-charset="ASCII" autocomplete="off">
  <table><tr><td>
  <input type="hidden" name="hidden_histo_name" value="{name}">
  <input type="text" name="histo_name" placeholder="quantity" \
         required=true value="{name}" {options}
         style="width:100%; box-sizing:border-box; -moz-box-sizing:border-box;">
  </td></tr><tr><td>
  <input type="text" name="title" placeholder="histo-title; x-title; y-title" \
         value="{title}" style="width:300px;">
  <input type="number" name="bins" placeholder="bins" style="width:40px;" \
         value="{bins}" min="1">
  <input type="number" name="low" placeholder="low" style="width:40px;" \
         step="0.01" value="{low}">
  <input type="number" name="high" placeholder="high" style="width:40px;" \
         step="0.01" value="{high}">
  <input type="submit" value="{button}">
  {datalist}
  </td></tr></table>
</form>
"""

base_selection_form = """\
<form method="post" id="sel-f">
  <input type="hidden" name="selection" value="">
</form>
"""

histo_selection_form = """\
<br />
<input type="number" name="{name} low" placeholder="low" style="width:40px;" \
       step="0.01" value="{low}" form="sel-f">
<input type="number" name="{name} high" placeholder="high" style="width:40px;" \
       step="0.01" value="{high}" form="sel-f">
<input type="submit" value="select events" form="sel-f">
"""

histo_form_args = {
    'name': '', 'title': '', 'bins': '', 'low': '', 'high': '',
    'options': 'id="input-histo-quantity" list="branchnames" autocomplete="on"',
    'button': 'create new',
    'datalist': '<datalist id="branchnames"></datalist>',
}

branch_loading_code = """
    function loadBranchNames() {
      // Get the <datalist> and <input> elements.
      var dataList = document.getElementById('branchnames');
      var input = document.getElementById('input-histo-quantity');
      input.placeholder = "quantity ...";

      // Create a new XMLHttpRequest.
      var request = new XMLHttpRequest();

      // Handle state changes for the request.
      request.onreadystatechange = function(response) {
        if (request.readyState === 4) {
          if (request.status === 200) {
            var jsonOptions = JSON.parse(request.responseText);

            jsonOptions.forEach(function(item) {
              var option = document.createElement('option');
              option.value = item;
              dataList.appendChild(option);
            });

            input.placeholder = "quantity";
          } else {
            input.placeholder = "quantity (no auto-comp.)";
          }
        }
      };

      // Set up and make the request.
      request.open('GET', '/branch_names.json', true);
      request.send();
    }
"""

figure_table_in = '<td><a href="#{var}">'
figure_table_out = '<td>{low}</td><td>{high}</td><td><a href="#{var}">'


def add_section_create_form(cont):
    placeholder = '<!-- SECTION CREATE FORM -->'
    form = section_form.format(button='create new')
    return cont.replace(placeholder, form)


def add_section_manipulate_forms(cont, section):
    placeholder = '<!-- SECTION UPDATE FORM -->'
    form = delete_form.format(
        action_dir='../', value='delete section', name=section)
    form += section_form.format(button='duplicate section')
    return cont.replace(placeholder, form)


def add_histo_create_form(cont):
    placeholder = '<!-- HISTO CREATE FORM -->'
    placeholder2 = '<!-- NO IMAGES -->'
    placeholder_java = '<!-- javascript -->'
    form = histo_form.format(**histo_form_args)
    cont = cont.replace('<body>', '<body onload="loadBranchNames()">',)
    cont = cont.replace(placeholder_java, branch_loading_code)
    if placeholder2 in cont:
        form = '<h2>Figures</h2>\ncreate new:<br />\n' + form
        return cont.replace(placeholder2, form)
    else:
        return cont.replace(placeholder, form)


def add_histo_manipulate_forms(cont, params, section_sel_info):
    sep = '<!-- IMAGE:'
    cont = cont.replace('rootjs.html?file=sections/', 'rootjs.html?file=')
    cont_parts = cont.split(sep)
    begin = [cont_parts.pop(0)]  # 'non-local' variable
    histos = params['histos']

    def add_selection_in_figure_tab(var, low, high):
        low = '>= %s &nbsp; &nbsp; ' % low if low else ''
        high = ' < %s &nbsp; &nbsp; ' % high if high else ''
        begin[0] = begin[0].replace(
            figure_table_in.format(var=var),
            figure_table_out.format(var=var, low=low, high=high)
        )

    def handle_histo_div(cont_part):
        if '<div class="img">' not in cont_part:
            return cont_part

        name = cont_part[:cont_part.find(':')]
        histo_params = histos.get(name, ('', '', '', ''))
        div_name = 'opt_' + name
        form_args = histo_form_args.copy()
        form_args.update({
            'name': name,
            'title': histo_params[0],
            'bins': histo_params[1],
            'low': histo_params[2],
            'high': histo_params[3],
            'options': 'disabled',
            'button': 'update',
            'datalist': '',
        })
        his_form = histo_form.format(**form_args)
        low, high = section_sel_info.get(name, ('', ''))
        sel_form = histo_selection_form.format(
            low=low, high=high, name=name)
        del_form = delete_form.format(
            value='delete histogram', name=name, action_dir='')
        toggle = '\n'.join((
            '<a href="javascript:ToggleDiv(\'%s\')">(toggle options)</a>'
            % div_name,
        ))
        div = '\n'.join((
            '<div id="%s" style="display:none;">' % div_name,
            his_form + del_form,
            '</div>',
        ))
        cont_part = cont_part.replace('<!-- TOGGLES -->', toggle)
        cont_part = cont_part.replace('<!-- TOGGLE_DIVS -->', div)
        cont_part = cont_part.replace('<!-- SELECTION FORM -->', sel_form)
        add_selection_in_figure_tab(name, low, high)
        return cont_part

    cont = sep.join(handle_histo_div(cp) for cp in cont_parts)
    return begin[0] + base_selection_form + sep + cont


def add_refresh(cont, timeout, url=''):
    tmplt = '<meta http-equiv="refresh" content="{};url={}">\n</head>'
    return cont.replace(
        '</head>',
        tmplt.format(str(int(timeout)), url)
    )
