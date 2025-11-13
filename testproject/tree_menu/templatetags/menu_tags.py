from django import template
from django.urls import reverse, NoReverseMatch
from tree_menu.models import MenuItem

register = template.Library()


@register.inclusion_tag('tree_menu/menu_template.html', takes_context=True)
def draw_menu(context, menu_name):
    """
    Строит дерево меню по имени menu_name.
    """
    request = context.get('request')
    current_url = request.path if request else ''


    items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent').order_by('order', 'name')


    children_map = {}
    for item in items:
        parent_id = item.parent.id if item.parent else None
        children_map.setdefault(parent_id, []).append(item)


    by_id = {item.id: item for item in items}


    def is_active_url(url):
        if not url:
            return False
        if url == current_url:
            return True
        if '/' not in url or ':' in url:
            try:
                resolved = reverse(url)
                return resolved == current_url
            except NoReverseMatch:
                return False
        return False


    active_id = None
    for item in items:
        if is_active_url(item.url):
            active_id = item.id
            break


    expanded = set()
    if active_id:
        parent = by_id[active_id].parent
        while parent:
            expanded.add(parent.id)
            parent = parent.parent
        expanded.add(active_id)
        for child in children_map.get(active_id, []):
            expanded.add(child.id)


    def build_tree(parent_id=None):
        result = []
        for item in children_map.get(parent_id, []):
            result.append({
                'item': item,
                'children': build_tree(item.id),
                'is_expanded': item.id in expanded,
                'is_active': item.id == active_id,
            })
        return result

    menu_tree = build_tree(None)

    return {
        'menu_tree': menu_tree,
        'menu_name': menu_name,
    }
