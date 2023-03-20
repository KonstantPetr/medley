import json


def compose_out_data(html_out_data_vector, pdf_out_data_vector, settings):
    
    out_keys = ('country',
                'named_bank',
                'info_bank',
                'product',
                'type_card',
                'purpose',
                'map_type',
                'currency',
                'condition_reg',
                'swift',
                'pay',
                'reg_cost',
                'maint_cost',
                'time_opening',
                'description',
                )
    
    out_data = []

    for bank_settings in settings:

        out_data.append({})
        pdf_count = 0

        for i, bank_setting in enumerate(bank_settings):

            if type(bank_setting) == dict:
                out_data[settings.index(bank_settings)][out_keys[i]] = \
                    pdf_out_data_vector[settings.index(bank_settings)][pdf_count]
                pdf_count += 1
            elif type(bank_setting) == list:
                out_data[settings.index(bank_settings)][out_keys[i]] = \
                    html_out_data_vector[settings.index(bank_settings)][i]
            else:
                out_data[settings.index(bank_settings)][out_keys[i]] = bank_setting

    return out_data


def dump_to_json(out_filename, data):
    with open(out_filename, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    pass
