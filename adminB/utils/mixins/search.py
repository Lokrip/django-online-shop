from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank
)

from .utils import logger

class Search:
    def __init__(self, model, query) -> None:
        self.model = model
        self.query = query

    def search(self):
        """
        Выполняет полнотекстовый поиск по заданной модели.

        Returns:
            QuerySet: Результаты поиска.

        Raises:
            ValueError: Если модель не определена или возникли проблемы при поиске.
            Exception: При других непредвиденных ошибках.
        """
        
        if not self.model:
            raise ValueError(logger(topic='database')[0])
        
        
        try:
            vector = SearchVector('title', 'description')
            query = SearchQuery(self.query)
            
            # rank в контексте полнотекстового поиска в Django (и в общем в системах поиска) означает 
            # оценку (или рейтинг) релевантности результата поиска. Он показывает, насколько хорошо 
            # документ (или запись в базе данных) соответствует заданному запросу
            results = self.model.objects.annotate(
                rank=SearchRank(vector, query)
            ).filter(
                rank__gt=0).order_by(
                    '-rank')
            
            if not results.exists():
                return "Product None"
            
            return results
                
        except Exception as e:
            # Ловим все непредвиденные ошибки и пробрасываем их дальше
            raise Exception(
                f"An unexpected error occurred: {
                    str(e)}"
            )
        
        except ValueError as VE:
            
            if VE in logger(
                topic='search'
                ):
                raise VE