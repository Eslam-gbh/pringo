from django.db import models


class StorageCustomManger(models.Manager):
    def get_available_storages(self, sku_dict):
        storages = self.get_stocked_storages_for_sku_ids(list(sku_dict.keys()))
        results, needs_to_be_fullfilled = self._get_available_storages(sku_dict, storages)
        assert needs_to_be_fullfilled < 1, f'Could not fullfill the order, current fullfiled {results}'
        return results

    def _get_available_storages(self, sku_dict, storages_query_set):
        sku_dict_copy = sku_dict.copy()
        results = []
        for storage in storages_query_set:
            storage_withrdawn_quantity = 0
            if sku_dict_copy[storage['sku__id']] > 0:

                if storage['stock'] >= sku_dict_copy[storage['sku__id']]:
                    storage_withrdawn_quantity = sku_dict_copy[storage['sku__id']]
                    sku_dict_copy[storage['sku__id']] = 0
                else:
                    sku_dict_copy[storage['sku__id']] -= storage['stock']
                    storage_withrdawn_quantity = storage['stock']

                results.append({
                    'id': storage['id'],
                    'quantity': storage_withrdawn_quantity
                })

        return results, sum(sku_dict_copy.values())

    def get_stocked_storages_for_sku_ids(self, sku_ids):
        return self.filter(sku_id__in=sku_ids, stock__gte=0)\
            .values('sku__id', 'id', 'stock')\
            .order_by('stock')
