from textual.widgets import RadioButton
from textual.widgets.selection_list import Selection


QUERY_SELECTIONS = [Selection('Subject', 'SubjectData', True),
                    Selection('MR Session', 'MrSessionData', False),
                    Selection('MR Scan', 'MrScanData', True),
                    Selection('CT Session', 'CtSessionData', False),
                    Selection('CT Scan', 'CtScanData', False),
                    Selection('US Session', 'UsSessionData', False),
                    Selection('US Scan', 'UsScanData', False),
                    ]

SEARCH_BASE_BUTTONS = [RadioButton('Subject'),
                       RadioButton('MrSession'),
                       RadioButton('MrScan', value=True),
                       RadioButton('CtSession'),
                       RadioButton('CtScan'),
                       RadioButton('UsSession'),
                       RadioButton('UsScan'),
                       ]

OPERATOR_OPTIONS = [('<', '<'),
                    ('<=', '<='),
                    ('=', '='),
                    ('!=', '!='),
                    ('>=', '>='),
                    ('>', '>'),
                    (' LIKE ', ' LIKE ')]
