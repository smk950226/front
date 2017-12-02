from django.shortcuts import render
from .utils import get_comic_info
from django.http import JsonResponse
from chartjs.views.lines import BaseLineChartView

def index(request):
    return render(request, 'chart/index.html')

'''
def data_json(request):
    comic = get_comic_info(20853, '마음의 소리')
    
    return JsonResponse({
        'labels': [ep['title'] for ep in comic['ep_list']],
        'datasets': [{
            'label': '평점',
            'backgroundColor': 'rgba(255, 99, 132, 0.5)',
            'borderColor': 'rgba(255, 99, 132, 1)',
            'pointBackgroundColor': 'rgba(255, 99, 132, 1)',
            'pointBorderColor': '#fff',
            'data': [ep['rating'] for ep in comic['ep_list']],
        }],
    })
'''

class WebtooonChartJSONView(BaseLineChartView):
    def __init__(self):
        super().__init__()
        self.comic = get_comic_info(20853, '마음의소리')
    
    def get_labels(self):
        return [ep['title'] for ep in self.comic['ep_list']]

    def get_providers(self):
        return ['평점']

    def get_data(self):
        return [
            [ep['rating'] for ep in self.comic['ep_list']],
        ]

    def get_colors(self):
        yield (255,99,132)


data_json = WebtooonChartJSONView.as_view()