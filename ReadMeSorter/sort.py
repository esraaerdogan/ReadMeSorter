def sort_blocks():
    # İlk olarak, mevcut README dosyasını belleğe yüklüyoruz
    with open('README.md', 'r') as read_me_file:
        read_me = read_me_file.read()
        
    # 'İçindekiler tablosunu' içeriklerden ayırma (bloklar)
    table_of_contents = ''.join(read_me.split('- - -')[0])
    blocks = ''.join(read_me.split('- - -')[1]).split('\n# ')
    for i in range(len(blocks)):
        if i == 0:
            blocks[i] = blocks[i] + '\n'
        else:
            blocks[i] = '# ' + blocks[i] + '\n'
    
    # Kütüphaneleri Sıralama
    inner_blocks = sorted(blocks[0].split('##'))
    for i in range(1, len(inner_blocks)):
        if inner_blocks[i][0] != '#':
            inner_blocks[i] = '##' + inner_blocks[i]
    inner_blocks = ''.join(inner_blocks)
    
    # Sıralanmamış kütüphaneleri sıralananlara göre değiştirmek 
    # ve hepsini gecici bir final_README dosyasında toplama
    blocks[0] = inner_blocks
    final_README = table_of_contents + '- - -' + ''.join(blocks)

    with open('README.md', 'w+') as sorted_file:
        sorted_file.write(final_README)

def main():
    # İlk olarak, geçerli README dosyasını bir satır dizisi olarak belleğe yüklüyoruz
    with open('README.md', 'r') as read_me_file:
        read_me = read_me_file.readlines()

    # Sonra çizgileri bloklar halinde bir araya getiriyoruz
    # Her blok, sıralanması gereken bir satır koleksiyonunu temsil eder
    # Bu sadece bağlantılar varsayılarak yapılıyor ([...](...)) sıralamak içindir
    # Kümeleme girinti ile yapılır
    blocks = []
    last_indent = None
    for line in read_me:
        s_line = line.lstrip()
        indent = len(line) - len(s_line)

        if any([s_line.startswith(s) for s in ['* [', '- [']]):
            if indent == last_indent:
                blocks[-1].append(line)
            else:
                blocks.append([line])
            last_indent = indent
        else:
            blocks.append([line])
            last_indent = None

    with open('README_sorted.md', 'w+') as sorted_file:
        # Sonra tüm bloklar ayrı ayrı sıralanır
        blocks = [
            ''.join(sorted(block, key=str.lower)) for block in blocks
        ]
        # Ve sonuç README.md dosyasına geri yazılır
        sorted_file.write(''.join(blocks))

    # Sonra sıralama yöntemini çağırırız
    sort_blocks()


if __name__ == "__main__":
    main()