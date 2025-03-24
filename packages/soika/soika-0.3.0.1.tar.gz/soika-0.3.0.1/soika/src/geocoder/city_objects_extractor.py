from typing import List
import re
import pandas as pd
from shapely.geometry import Point, Polygon, MultiPolygon
from loguru import logger
import pymorphy2
from soika.src.utils.constants import NUM_CITY_OBJ
from soika.src.geocoder.objects_address_extractor_by_rules import AddressExtractorExtra
from soika.src.utils.data_getter.geo_data_getter import GeoDataGetter
from rapidfuzz import fuzz
import numpy as np
from tqdm import tqdm
tqdm.pandas()

class OtherGeoObjects:
    @staticmethod
    def get_and_process_osm_data(osm_id: int, tags: dict) -> pd.DataFrame:
        """
        Retrieves and processes OSM data for different urban objects.
        """
        df = GeoDataGetter.get_osm_data(osm_id, tags)
        df["geometry"] = df["geometry"].progress_apply(OtherGeoObjects.calculate_centroid)
        df.rename(columns={df.columns[-1]: "geo_obj_tag"}, inplace=True)
        return df

    @staticmethod
    def run_osm_dfs(osm_id: int) -> pd.DataFrame:
        """
        Collects dataframes with OSM spatial data, finds centroids and combines them into one.
        """
        tags_list = [
            {"leisure": ["park", "garden", "recreation_ground"]},
            {"amenity": ["hospital", "clinic", "school", "kindergarten"]},
            {"landuse": ["cemetery"]},
            {"natural": ["beach", "water"]},
            {"railway": ["station", "subway"]},
            {"tourism": ["attraction", "museum"]},
            {"historic": ["monument", "memorial"]},
            {"place": ["square"]},
        ]
        
        osm_dfs = list()
        for tags in tags_list:
            logger.debug(f'getting {osm_id, tags}')
            try:
                tmp_df = OtherGeoObjects.get_and_process_osm_data(osm_id, tags)
                osm_dfs.append(tmp_df)
            except RuntimeError:
                logger.warning(f'Runtime error during fetching {osm_id, tags}')
                continue
        if osm_dfs:
            osm_combined_df = pd.concat(osm_dfs, axis=0)
            logger.debug(f'got {osm_id, tags}')
            logger.debug(f'{osm_combined_df.shape}')
            return osm_combined_df
        else:
            logger.warning(f'No data were gathered about city objects in {osm_id}')
            return pd.DataFrame()

    @staticmethod
    def calculate_centroid(geometry) -> Point:
        """
        Calculates the centroid for polygons.
        """
        if isinstance(geometry, (Polygon, MultiPolygon)):
            return geometry.centroid
        elif isinstance(geometry, Point):
            return geometry
        else:
            return None

    @staticmethod
    def extract_geo_obj(text, morph=None, extractor=None) -> List[str]:
        """
        Extracts location entities from the text using the Natasha library.
        """
        if not text:
            return []

        # Avoid repeated initialization of heavy objects
        if morph is None:
            morph = pymorphy2.MorphAnalyzer()
        if extractor is None:
            extractor = AddressExtractorExtra(morph)

        try:
            matches = extractor(text)
            if not matches:
                return []

            return [
                f"{match.fact.value} {match.fact.type}".strip()
                for match in matches if match and match.fact
            ]
        except Exception:
            return []


    @staticmethod
    def restoration_of_normal_form(other_geo_obj, osm_combined_df, threshold=0.7) -> List[str]:
        """
        This function compares the extracted location entity with an OSM array
        and returns a normalized form if the percentage of similarity is at least 70%.
        """
        osm_name_obj = osm_combined_df["name"].tolist()
        similarity_matrix = np.zeros((len(other_geo_obj), len(osm_name_obj)))

        def extract_numbers(s):
            return re.findall(r"\d+", s)
        
        percents = 100

        for i, word1 in enumerate(other_geo_obj):
            numbers_from_extraction = extract_numbers(word1)
            for j, word2 in enumerate(osm_name_obj):
                numbers_from_OSM_name = extract_numbers(word2)
                if numbers_from_extraction == numbers_from_OSM_name:
                    similarity = fuzz.ratio(word1, word2) / percents
                else:
                    similarity = 0
                similarity_matrix[i, j] = similarity

        restoration_list = other_geo_obj.copy()
        for i in range(len(other_geo_obj)):
            max_index = np.argmax(similarity_matrix[i])
            if similarity_matrix[i, max_index] > threshold:
                restoration_list[i] = osm_name_obj[max_index]
            else:
                restoration_list[i] = ""

        return restoration_list

    @staticmethod
    def find_num_city_obj(text) -> List[str]:
        """
        This function searches for urban objects in the text,
        the names of which are represented as a number. For example, "school No. 6".
        """
        text = str(text)
        text = text.lower()
        num_obj_list = []
        for key, forms in NUM_CITY_OBJ.items():
            for form in forms:
                pattern = rf"\b{re.escape(form)}\b\s+№?\s*(\d+)"
                matches = re.findall(pattern, text)
                for match in matches:
                    num_obj_list.append(f"{key} № {match}")
        num_obj_list = list(set(num_obj_list))
        num_obj_list_clear = {}
        for obj in num_obj_list:
            key = obj.split(" № ")[1]
            if key in num_obj_list_clear:
                if len(obj.split(" № ")[0]) > len(num_obj_list_clear[key].split(" № ")[0]):
                    num_obj_list_clear[key] = obj
            else:
                num_obj_list_clear[key] = obj

        return list(num_obj_list_clear.values())

    @staticmethod
    def combine_city_obj(df_obj) -> pd.DataFrame:
        """
        Combines the found named urban objects and urban objects whose names are in the form of numbers.
        """
        df_obj["other_geo_obj"] = df_obj["other_geo_obj"] + df_obj["other_geo_obj_num"]
        df_obj.drop(columns=["other_geo_obj_num"], inplace=True)
        return df_obj

    @staticmethod
    def expand_toponym(df_obj) -> pd.DataFrame:
        """
        Splits the list of found entities into different rows for further analysis.
        """
        expanded_df = df_obj.copy()
        expanded_df["other_geo_obj"] = expanded_df["other_geo_obj"].apply(
            lambda x: x if isinstance(x, list) and x else None
        )
        expanded_df = expanded_df.explode("other_geo_obj").reset_index(drop=True)
        return expanded_df

    @staticmethod
    def find_geometry(toponym, osm_combined_df) -> Point:
        """
        Finds the coordinate in the OSM array by the name of the city object.
        """
        if toponym is None:
            return None
        match = osm_combined_df[osm_combined_df["name"] == toponym]
        if not match.empty:
            return match.iloc[0, 1]
        else:
            return None

    @staticmethod
    def find_geo_obj_tag(toponym, osm_combined_df) -> str:
        """
        Finds the geo_obj_tag in the OSM array by the name of the city object.
        """
        if toponym is None:
            return None
        match = osm_combined_df[osm_combined_df["name"] == toponym]
        if not match.empty:
            return match.iloc[0, -1]
        else:
            return None

    @staticmethod
    def get_unique_part_types(df):
        return df["other_geo_obj"].unique()

    @staticmethod
    def run(osm_id: int, df: pd.DataFrame, text_column: str) -> pd.DataFrame:
        """
        Launches the module for extracting urban objects from texts that do not relate to streets.
        """
        df_obj = df.copy()
        df_obj["Numbers"] = pd.NA
        # osm_combined_df = OtherGeoObjects.run_osm_dfs(osm_id)
        print('Extracting objects')
        df_obj["other_geo_obj"] = df_obj[text_column].progress_apply(OtherGeoObjects.extract_geo_obj)
        print("Searching for object numbers")
        df_obj["other_geo_obj_num"] = df_obj[text_column].progress_apply(
            lambda x: OtherGeoObjects.find_num_city_obj(x)
        )
        
        df_obj = OtherGeoObjects.combine_city_obj(df_obj)

        print("Collecting OSM data")
        osm_combined_df = OtherGeoObjects.run_osm_dfs(osm_id)

        if not osm_combined_df.empty:
            print("restoring normal form of objects")
            df_obj["other_geo_obj"] = df_obj["other_geo_obj"].progress_apply(
                lambda x: OtherGeoObjects.restoration_of_normal_form(x, osm_combined_df)
            )
            df_obj = OtherGeoObjects.expand_toponym(df_obj)

            print("Matching objects and geometries")
            df_obj["geometry"] = df_obj["other_geo_obj"].apply(lambda x: OtherGeoObjects.find_geometry(x, osm_combined_df))
            df_obj["geo_obj_tag"] = df_obj["other_geo_obj"].apply(
                lambda x: OtherGeoObjects.find_geo_obj_tag(x, osm_combined_df)
            )
            df_obj = df_obj[df_obj["geometry"].notna()]

        return df_obj
