from bs4 import BeautifulSoup
import pandas as pd
import sys


def write_df(df, path):
    with open(path, 'w', encoding='utf-8') as file:
        df.to_json(file, orient='records', force_ascii=False)


def get_method_detail(file_path, package_name, class_name, type, method_index):
    f = open(file_path, 'r', encoding='utf-8')
    method_detail_soup = BeautifulSoup(f, "lxml")
    f.close()
    method_summary = method_detail_soup.find("table", {"class": "memberSummary",
                                                       'summary': 'Method Summary table, listing methods, and an explanation'})
    temp_soup = BeautifulSoup(str(method_summary), "lxml")
    altColorList = temp_soup.find_all("tr", {"class": "altColor"})
    rowColorList = temp_soup.find_all("tr", {"class": "rowColor"})
    for altColor in altColorList:
        temp_color_soup = BeautifulSoup(str(altColor), "lxml")

        col_first_text = ''
        col_second_text = ''
        col_last_text = ''
        colFirst = temp_color_soup.find(attrs={"class": "colFirst"})
        if colFirst is not None:
            col_first_text = colFirst.get_text()

        colSecond = temp_color_soup.find(attrs={"class": "colSecond"})
        if colSecond is not None:
            col_second_text = colSecond.get_text()

        colLast = temp_color_soup.find(attrs={"class": "colLast"})
        if colLast is not None:
            col_last_text = colLast.get_text()
        if col_second_text is not None:
            method_detail_df.loc[method_index] = [package_name, class_name, col_first_text, col_second_text,
                                                  col_last_text,
                                                  type]
            method_index += 1

    for altColor in rowColorList:
        temp_color_soup = BeautifulSoup(str(altColor), "lxml")

        col_first_text = ''
        col_second_text = ''
        col_last_text = ''
        colFirst = temp_color_soup.find(attrs={"class": "colFirst"})
        if colFirst is not None:
            col_first_text = colFirst.get_text()

        colSecond = temp_color_soup.find(attrs={"class": "colSecond"})
        if colSecond is not None:
            col_second_text = colSecond.get_text()

        colLast = temp_color_soup.find(attrs={"class": "colLast"})
        if colLast is not None:
            col_last_text = colLast.get_text()
        if col_second_text is not None:
            method_detail_df.loc[method_index] = [package_name, class_name, col_first_text, col_second_text,
                                                  col_last_text,
                                                  type]
            method_index += 1
    return method_index


def get_package_detail_info(file_path, package_name, detail_index, method_index):
    f = open(file_path, encoding="utf8")
    package_detail_soup = BeautifulSoup(f, "lxml")
    f.close()
    li_block_list = package_detail_soup.findAll("li", {"class": "blockList"})
    for li_block in li_block_list:
        temp_soup = BeautifulSoup(str(li_block), "lxml")
        first_span = temp_soup.find('span')
        type_string = first_span.get_text()
        print(type_string)
        type = d[type_string]
        altColorList = temp_soup.findAll("tr", {"class": "altColor"})
        rowColorList = temp_soup.findAll("tr", {"class": "rowColor"})
        for altColor in altColorList:
            temp_soup = BeautifulSoup(str(altColor), "lxml")
            colFirst = temp_soup.find("a")
            name = colFirst.get_text()
            url = colFirst['href']
            url = url.split('../')[-1]
            description = ''
            colLast = temp_soup.find(attrs={"class": "block"})
            if colLast is not None:
                description = colLast.get_text()
            df.loc[detail_index] = [package_name, name, url, description, type]
            method_index = get_method_detail(base_path + url, package_name, name, type, method_index)
            detail_index += 1

        for rowColor in rowColorList:
            temp_soup = BeautifulSoup(str(rowColor), "lxml")
            colFirst = temp_soup.find("a")
            name = colFirst.get_text()
            url = colFirst['href']
            url = url.split('../')[-1]
            description = ''
            colLast = temp_soup.find(attrs={"class": "block"})
            if colLast is not None:
                description = colLast.get_text()
                df.loc[detail_index] = [package_name, name, url, description, type]
                method_index = get_method_detail(base_path + url, package_name, name, type, method_index)
            detail_index += 1
    return detail_index, method_index


if __name__ == "__main__":
    d = {'Interface Summary': 0, 'Class Summary': 1, 'Enum Summary': 2, 'Exception Summary': 3,
         'Annotation Types Summary': 4}
    detail_index = 0
    method_index = 0
    df = pd.DataFrame(columns=['package_name', 'name', 'url', 'description', 'type'])
    method_detail_df = pd.DataFrame(
        columns=['package_name', 'class_name', 'returnType', 'Method', 'description', 'type'])

    base_path = 'D:/project/poi_html_full/'
    file_path = base_path + 'overview-summary.html'
    f = open(file_path)
    soup = BeautifulSoup(f, "lxml")
    f.close()
    altColorList = soup.findAll("tr", {"class": "altColor"})
    rowColorList = soup.findAll("tr", {"class": "rowColor"})
    package_df = pd.DataFrame(columns=['package_name', 'package_url', 'description'])
    package_index = 0

    for altColor in altColorList:
        temp_soup = BeautifulSoup(str(altColor), "lxml")
        colFirst = temp_soup.find("a")
        package_name = colFirst.get_text()
        package_url = colFirst['href']
        description = ''
        colLast = temp_soup.find(attrs={"class": "block"})
        if colLast is not None:
            description = colLast.get_text()
        package_df.loc[package_index] = [package_name, package_url, description]
        detail_index, method_index = get_package_detail_info(base_path + package_url, package_name, detail_index,
                                                             method_index)
        package_index += 1

    for rowColor in rowColorList:
        temp_soup = BeautifulSoup(str(rowColor), "lxml")
        colFirst = temp_soup.find("a")
        package_name = colFirst.get_text()
        package_url = colFirst['href']
        description = ''
        colLast = temp_soup.find(attrs={"class": "block"})
        if colLast is not None:
            description = colLast.get_text()
        package_df.loc[package_index] = [package_name, package_url, description]
        detail_index, method_index = get_package_detail_info(base_path + package_url, package_name, detail_index,
                                                             method_index)
        package_index += 1
    write_df(package_df, 'packages.json')
    write_df(df, 'package_detail.json')
    write_df(method_detail_df, 'method_detail_df.json')
