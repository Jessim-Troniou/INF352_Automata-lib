from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, ListStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem


def generate_pdf(output_path='exercice_33_solution.pdf'):
    styles = getSampleStyleSheet()
    normal = styles['BodyText']
    normal.fontName = 'Helvetica'
    normal.fontSize = 12
    normal.leading = 16

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        spaceAfter=20,
        alignment=1,
    )

    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['BodyText'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        spaceBefore=10,
        spaceAfter=6,
    )

    doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    list_style = ListStyle('ListStyle', bulletType='bullet', leftIndent=20, bulletIndent=10, fontName='Helvetica', fontSize=11, leading=14)

    story.append(Paragraph('Exercice 33 — Déterminer si un automate est minimal ou non', title_style))
    story.append(Paragraph('Nous considérons les deux automates de la Figure 6.3. Nous voulons déterminer s’ils sont minimaux. Pour chacun d’eux, on applique les deux méthodes :', normal))

    story.append(Paragraph('1. Méthode des états distinguables', subtitle_style))
    story.append(Paragraph('Pour d1, la relation de distinguabilité contient les paires : (1,2), (1,3), (1,4), (2,1), (2,3), (2,4), (3,1), (3,2), (3,4), (4,1), (4,2), (4,3).', normal))
    story.append(Paragraph('Pour d2, les paires distinguables sont toutes les paires entre états de classes distinctes; on trouve notamment (1,5), (5,1), (2,4), (4,2), (3,6), (6,3).', normal))

    story.append(Paragraph('2. Méthode des classes d’équivalence', subtitle_style))
    story.append(Paragraph('Les classes d’équivalence sont :', normal))
    story.append(ListFlowable([
        ListItem(Paragraph('d1 : [[1], [2], [3], [4]]', normal)),
        ListItem(Paragraph('d2 : [[1,5], [2,4], [3,6]]', normal)),
    ], bulletType='bullet', style=list_style))

    story.append(Paragraph('3. Vérification des conclusions', subtitle_style))
    story.append(Paragraph('On obtient la même conclusion par les deux méthodes :', normal))
    story.append(ListFlowable([
        ListItem(Paragraph('d1 est minimal : chaque état est distinct; aucune fusion n’est possible.', normal)),
        ListItem(Paragraph('d2 n’est pas minimal : 1 ≡ 5, 2 ≡ 4 et 3 ≡ 6. On peut fusionner ces états.', normal)),
    ], bulletType='bullet', style=list_style))

    story.append(Paragraph('4. Représentation de l’automate minimal', subtitle_style))
    story.append(Paragraph('Automate minimal de d1 : on garde les 4 états originaux, car ils sont tous distinguables.', normal))
    story.append(Paragraph('Automate minimal de d2 : on fusionne 1 et 5 en A, 2 et 4 en B, 3 et 6 en C. La table de transition devient :', normal))
    story.append(Paragraph('       0         1', normal))
    story.append(Paragraph('A -> C     ; A -> B', normal))
    story.append(Paragraph('B -> A     ; B -> C', normal))
    story.append(Paragraph('C -> C     ; C -> C', normal))
    story.append(Paragraph('État initial : A ; états finaux : {A}.', normal))

    doc.build(story)
    print(f'PDF generated: {output_path}')


if __name__ == '__main__':
    generate_pdf()
