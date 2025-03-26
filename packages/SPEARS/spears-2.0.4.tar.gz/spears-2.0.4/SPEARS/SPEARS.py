# =============================================================================
# Import Statements
# =============================================================================

# Standard Library Imports
import os  # For file and directory operations
import warnings  # For handling warnings
import time  # For time-related operations
from timeit import default_timer as timer  # For precise timing
from datetime import timedelta  # For time duration calculations
import json  # For JSON file handling
import concurrent.futures  # For multithreading
import importlib.resources as pkg_resources # For accessing line data within library

# Third-Party Library Imports
from sparcl.client import SparclClient  # SPARCL API client
from specutils import Spectrum1D  # For spectral data representation
from specutils.fitting import find_lines_derivative  # For spectral line detection
from astropy import units as u  # For unit handling
from astropy.table import QTable, vstack  # For tabular data handling
from astropy.io import fits  # For FITS file handling
from scipy.ndimage import median_filter  # For median filtering
from alive_progress import alive_bar  # For progress bars
import numpy as np  # For numerical operations
import bisect  # For binary search operations
import specutils  # For additional spectral utilities


# =============================================================================
# Version Notes
# =============================================================================

# NOTE: Version 2 Improvements
    # Introduced the SPEAR class, storing local variables instead of utilizing functions
    # Massively improved computational effecientcy
    # Better improved modularity, and client-side customization
    # Improved simplicity and ease-of-use
    # (actually works well)
    # Officially supports simple multithreading
    # So much more, a complete rehaul from V1

# NOTE: Version 2.1 - to do
    # Complete a full check for errors
        # Check for error if # ids / threads < 1

# NOTE: Version 3 - to do
    # Fully support other datsets in SPARCL
    # Extend support outside the SPARCL API
    # Improve effecientcy
    # Implement out-of-terminal viewers 
        # Implement a FITS table viewer
    # Vectorize computation to run on GPU
    # Support multithreading progress bars
    # Change format to multithread process

# =============================================================================
# SPEAR Class
# =============================================================================
class SPEAR():
    """
    SPEAR: SPARCL Pipeline for Emission Absorption line Retrieval Spectroscopy

    A class for processing and analyzing spectral data from the SPARCL database.

    This class provides a comprehensive pipeline for downloading, normalizing, detecting spectral lines,
    visualizing spectral data, and saving results. It supports both single-threaded and multithreaded 
    execution for enhanced performance and scalability.

    Key Features:
        - Integration with the SPARCL API for spectral data retrieval.
        - Multithreaded processing for improved computational efficiency.
        - Spectral normalization using median filtering with adaptive kernel sizes.
        - Spectral line detection with detailed metadata packaging.
        - Visualization tools for raw, normalized, and line-detected spectra.
        - FITS file export for analysis results.
        - Modular design for extensibility and client-side customization.
        - Detailed time reporting for performance analysis.

    Attributes:
        client (SparclClient): Client for retrieving data from the SPARCL database (not instantiated for threads).
        SPARCL_ids (list): List of SPARCL IDs for data retrieval.
        spectrum1d_array (list): List of Spectrum1D objects representing raw spectral data.
        normalized_spectra (list): List of Spectrum1D objects representing normalized spectral data.
        results (QTable): Results of spectral line detection and metadata packaging.
        dict_results (dict): Results of spectral line detection in dictionary format.
        dataset (list): Dataset identifier(s) for the SPARCL API.
        multithreading (bool): Flag indicating whether multithreading is enabled.
        thread_classes (list): List of SPEAR instances for multithreaded processing.
        thread_allocation (int): Number of threads allocated for analysis.
        download_time (timedelta): Time taken for data download.
        format_time (timedelta): Time taken for data formatting.
        normalization_time (timedelta): Time taken for spectral normalization.
        normalization_time_STD (float): Standard deviation of normalization time across threads.
        detection_packaging_time (timedelta): Time taken for line detection and packaging.
        detection_packaging_time_STD (float): Standard deviation of detection packaging time across threads.
        total_time (timedelta): Total elapsed time for the analysis process.
        program_start (float): Timestamp marking the start of program execution.
        flux_unit (str): Unit for spectral flux values.
        lines_info (dict): Dictionary containing known emission line information.
        line_wavelengths (list): Sorted list of emission line wavelengths.
        supported_datasets (list): List of supported dataset names.
        spectrum_variability_values (dict): Values related to spectrum variability for normalization.
        spectral_resolution_values (dict): Parameters defining the spectral resolution function.
        include_progress_bar (bool): Determines whether to include progress bars in terminal output.
        is_thread (bool): Indicates whether the instance is part of a multithreaded process.
    """

    def __init__(self, SPARCL_ids: list = None, is_thread = False, include_progress_bar = True) -> None:
        """
        Initializes the SPEAR instance.

        Instantiates the SparclClient and loads emission line info from a JSON file.
        NOTE: Fix to load within library

        Args:
            SPARCL_ids (list, optional): List of SPARCL IDs to process. Defaults to None.

        Returns:
            None
        """

        try:
            with pkg_resources.open_text("spears.data", "emission_lines.json") as f:
                lines_info = json.load(f)
        except Exception as e:
            print('Error in __init__ when loading emission line data from json: ', e)

        # Public Variables
        if not is_thread:
            self.client = SparclClient()
        self.is_thread = is_thread
        if include_progress_bar:
            self.include_progress_bar = True
        else:
            self.include_progress_bar = False
        self.SPARCL_ids = SPARCL_ids
        self.spectrum1d_array = None
        self.normalized_spectra = None
        self.results = None
        self.dataset = None
        self.multithreading = False
        self.thread_classes = []
        self.threads = []
        self.thread_allocation = 1
        self.dict_results = None
        # Report Metrics
        self.download_time = timedelta(seconds=0)
        self.format_time = timedelta(seconds=0)
        self.normalization_time = timedelta(seconds=0)
        self.detection_packaging_time = timedelta(seconds=0)
        self.normalization_time_STD = 0
        self.detection_packaging_time_STD = 0
        self.start_time = time.time()

        # Private Variables
        self.program_start = timer()
        self.flux_unit = '1 / (erg17 cm2 s Angstrom)'
        self.lines_info = lines_info
        self.line_wavelengths = sorted([float(key) for key in lines_info.keys()])
        self.supported_datasets = ['BOSS-DR16', 'BOSS-DR17', 'DESI-DR1', 'DESI-EDR', 'SDSS-DR16', 'SDSS-DR17', 'SDSS-DR17-test', 'DESI', 'SDSS_BOSS']

        # NOTE: SPECFIC TO THE DESI-EDR
        self.spectrum_variability_values = {"standard_deviation" : 0.260,
                                       "mean" : 0.376}
        
        self.spectral_resolution_values = {"slope" : -3.23e-5,
            "y-intercept" : 1.78
        }

    # -----------------------------------------------------------------------------
    def get_threads(self):
        """
        Returns the number of threads available to the system.

        Returns:
            int: Number of available CPU threads.
        """
        return os.cpu_count()
    
    # -----------------------------------------------------------------------------
    def init_multithreading(self, thread_allocation: int):
        """
        Initializes the multithreading environment with a specified thread allocation.

        This method checks if the allocated number of threads exceeds the available CPU threads,
        issues warnings if all threads are allocated, and splits the SPARCL_ids for multithreaded processing.
        
        Args:
            thread_allocation (int): The number of threads to allocate.

        Returns:
            None

        Raises:
            ValueError: If the allocated threads exceed the available CPU threads.
        """
        # Raises errors/warnings for thread allocation
        if thread_allocation > os.cpu_count():
            raise ValueError(f"Allocated {thread_allocation}/{os.cpu_count()} available threads. Please reallocate a proper amount.")
        elif thread_allocation <= 1:
            raise ValueError(f'Allocated threads cannot be less than or equal to 1, for a single thread do not utilize init_multithreading() simply utilize analyze(), given value: ', thread_allocation)
        elif thread_allocation == os.cpu_count():
            warnings.warn("WARNING: Allocating all threads available, could result in OS instability and thread oversubscription \n Unless you are sure, please re-start and allocate less threads.")
            if input('Would you like the continue with full threading? (Y/N): ').upper() == 'N':
                return
        
        
        # Warning for progress bar
        if self.include_progress_bar:
            print('NOTE: Progress bars may slightly impact performance, for best performance disable in __init__ argument. Metrics can still be accessed post-processing via the __str__() or the time_report() function.')
            print('NOTE: currently implementation for progress bars only exists for the __download() function for multithreaded processes')

        # Downloads all spectra at once to avoid API errors
        self.thread_allocation = thread_allocation

        # Attemps download from API
        try:
            self.__download()
        except Exception as e:
            print('Error in init_mulithreading SPARCL spectra download: ', e)

        # Instantiate an array of threads, each a class with respective spectra      
        spectrum_blocks = np.array_split(self.spectrum1d_array, thread_allocation)
        id_blocks = np.array_split(self.SPARCL_ids, thread_allocation)

        # Instantiates classes for each id with respective loads
        try:
            for i in range(len(spectrum_blocks)):
                self.thread_classes.append(SPEAR(is_thread = True))
                self.thread_classes[i].set_SPARCL_ids(id_blocks[i].tolist())
                self.thread_classes[i].__set_spectrum1D_array(spectrum_blocks[i].tolist())
        except Exception as e:
            print('Error in init_multithreading appending spectrum_1D blocks to thread classes: ', e)

        self.multithreading = True

    # -----------------------------------------------------------------------------
    def analyze(self):
        """
        Analyzes the spectral data using either single-threaded or multithreaded processing.

        Depending on the multithreading flag, this method invokes the appropriate analysis 
        method to process spectral data (download, normalization, and line detection).

        Returns:
            The analysis results (typically a QTable) stored in the `results` attribute.
        """
        if self.multithreading == False:
            self.__singlethreaded_analyze()
        else:
            self.__multithreaded_analyze()
        
        # Optionally returns results
        return self.results
    
    # -----------------------------------------------------------------------------
    def save_to_fits(self, filename: str, path: str):
        """
        Saves the analysis results to a FITS file.

        This method writes the QTable results to a FITS file, processing each table column
        to ensure string data is converted to ASCII.

        Args:
            filename (str): The name of the FITS file.
            path (str): The directory path where the FITS file will be saved.

        Returns:
            None

        Raises:
            AttributeError: If no analysis results exist.
            RuntimeError: If an error occurs during the saving process.
        """
        # NOTE: handle improper filenames/paths propertly
        # NOTE: Doesn't work
        if self.results is None:
            raise AttributeError("No analysis has been made to save; run analyze() prior to save_to_fits")
        
        try:
            hdul = fits.HDUList([fits.PrimaryHDU()])
            # Iterate over each QTable stored in self.results['data']
            for i, qt in enumerate(self.results["data"]):
                # Make a copy so we don't alter the original table
                qt_copy = qt.copy()
                # Process each column that might contain strings
                for col in qt_copy.colnames:
                    # Check if the column is of a string type.
                    if qt_copy[col].dtype.kind in "UO":  # Unicode or object type that may contain strings
                        # Convert each element to ASCII by ignoring non-ASCII characters
                        qt_copy[col] = [s.encode("ascii", "ignore").decode("ascii") if isinstance(s, str) else s 
                                        for s in qt_copy[col]]
                hdu = fits.BinTableHDU(qt_copy, name=f"Spectrum_{i}")
                hdul.append(hdu)
            
            filepath = os.path.join(path, filename)
            hdul.writeto(filepath, overwrite=True)
            print(f"Results saved to {filepath}")
        except Exception as e:
            raise RuntimeError(f"Error occurred in save_to_fits(): {str(e)}")

    # -----------------------------------------------------------------------------
    def visualize_test(self):
        """
        Visualizes test spectral data through a series of plots.

        This method sets a predefined list of test SPARCL IDs, runs the analysis,
        and then displays three sets of plots:
            1. Raw spectra.
            2. Normalized spectra.
            3. Spectra with detected spectral lines.
        
        Returns:
            None

        Raises:
            ValueError: If the required spectral data is missing.
        """
        self.SPARCL_ids = ['00001edd-9d21-11ee-80af-525400ad1336', '00003408-9cd1-11ee-935e-525400ad1336', '00003edd-9bea-11ee-b77b-525400ad1336', '00006b52-9b41-11ee-8303-525400ad1336', '00008539-9c07-11ee-a0f0-525400ad1336', '0000a7a7-9bd6-11ee-a1da-525400ad1336', '0000b61b-9af9-11ee-bb33-525400ad1336', '0000bb12-9d55-11ee-a8dc-525400ad1336', '0000bd71-9b38-11ee-853e-525400ad1336', '000147cc-9c6f-11ee-9d98-525400ad1336']
        self.analyze()

        import matplotlib.pyplot as plt

        # Ensure spectra are available
        if self.spectrum1d_array is None or self.normalized_spectra is None or self.results is None:
            raise ValueError("Spectra data is missing. Ensure analyze() has been run before visualization.")

        # Create a 3x2 grid for subplots
        fig, axes = plt.subplots(3, 2, figsize=(15, 15))
        axes = axes.flatten()

        try:
            # Plot raw spectra
            for i, spectrum in enumerate(self.spectrum1d_array[:6]):
                ax = axes[i]
                ax.plot(spectrum.spectral_axis, spectrum.flux, label="Raw Spectrum")
                ax.set_title(f"Raw Spectrum {i+1}")
                ax.set_xlabel("Wavelength (Å)")
                ax.set_ylabel("Flux")
                ax.legend()

            plt.tight_layout()
            plt.pause(5)  # Pause for 5 seconds

            # Clear the plots for the next set
            for ax in axes:
                ax.clear()

            # Plot normalized spectra
            for i, spectrum in enumerate(self.normalized_spectra[:6]):
                ax = axes[i]
                ax.plot(spectrum.spectral_axis, spectrum.flux, label="Normalized Spectrum", color="orange")
                ax.set_title(f"Normalized Spectrum {i+1}")
                ax.set_xlabel("Wavelength (Å)")
                ax.set_ylabel("Normalized Flux")
                ax.legend()

            plt.tight_layout()
            plt.pause(5)  # Pause for 5 seconds

            # Clear the plots for the next set
            for ax in axes:
                ax.clear()

            # Plot spectra with detected lines
            for i, spectrum in enumerate(self.normalized_spectra[:6]):
                ax = axes[i]
                ax.plot(spectrum.spectral_axis, spectrum.flux, label="Spectrum with Lines", color="green")
                detected_lines = self.results['data'][i]['observed_wavelength']
                for line in detected_lines:
                    ax.axvline(line.value, color="red", linestyle="--", alpha=0.7, label="Detected Line" if line == detected_lines[0] else "")
                ax.set_title(f"Spectrum with Detected Lines {i+1}")
                ax.set_xlabel("Wavelength (Å)")
                ax.set_ylabel("Normalized Flux")
                ax.legend()

            plt.tight_layout()
            plt.show()
        except Exception as e:
            print('Error plotting visualizer data in visualize_test(): ', e)

    # -----------------------------------------------------------------------------
    def __str__(self):
        """
        Returns a string summary of the SPEAR object's current state.

        The summary includes the counts of SPARCL IDs ingested, downloaded spectra,
        normalized spectra, analysis results, and the multithreading status.

        Returns:
            str: A summary string describing the current state.
        """
        try:
            report = self.get_time_report()
            string = f"""
                            Records Ingested: {len(self.SPARCL_ids) if self.SPARCL_ids else 0}
                            Downloaded: {len(self.spectrum1d_array) if self.spectrum1d_array else 0}
                            Normalized: {len(self.normalized_spectra) if self.normalized_spectra else 0}
                            Results: {len(self.results) if self.results else 0}
                            Thread Utilized: {self.thread_allocation}
                            Time Report
                            __________________________________________
                        {report}
                    """
            return string
        except Exception as e:
            print('Error occured in __str__: ', e)

    # =============================================================================
    # Getter and Setter Methods
    # =============================================================================
    def get_spectrum(self):
        """
        Returns the raw Spectrum1D array.

        Returns:
            list: List of Spectrum1D objects representing raw spectral data.
        """
        return self.spectrum1d_array
    
    # -----------------------------------------------------------------------------
    def get_time_report(self):
        """
        Generates a detailed time report for various stages of the process.

        This method calculates and formats the elapsed time for different stages 
        such as downloading, formatting, normalization, and line detection & data 
        packaging. It accounts for whether multithreading is enabled or not and 
        adjusts the report accordingly.

        Returns:
            str: A formatted string containing the time report. The report includes:
                - Download Time
                - Formatting Time
                - Normalization Time (with mean and standard deviation if multithreading is enabled)
                - Line Detection & Data Packaging Time (with mean and standard deviation if multithreading is enabled)
                - Non-Download Total Elapsed Time
                - Total Elapsed Time

        Raises:
            Exception: If an error occurs during the generation of the time report, 
                       it prints an error message with the exception details.
        """
        try:
            # Checks multithreading to account for averaged times
            if not self.multithreading:
                report = f"""
                            Download Time: {self.download_time.total_seconds() / 60:.2f} minutes
                            Formatting Time: {self.format_time.total_seconds() / 60:.2f} minutes
                            Normalization Time: {self.normalization_time.total_seconds() / 60:.2f} minutes
                            Line Detection & Data Packaging Time: {self.detection_packaging_time.total_seconds() / 60:.2f} minutes
                            Non-Download Total Elapsed Time: {(self.format_time.total_seconds() + self.normalization_time.total_seconds() + self.detection_packaging_time.total_seconds()) / 60:.2f} minutes
                            Total Elapsed Time: {(self.download_time.total_seconds() + self.format_time.total_seconds() + self.normalization_time.total_seconds() + self.detection_packaging_time.total_seconds()) / 60:.2f} minutes
                            """
            else:
                report = f"""
                            Download Time: {self.download_time.total_seconds() / 60:.2f} minutes
                            Formatting Time: {self.format_time.total_seconds() / 60:.2f} minutes
                            Thread-Mean Normalization Time: {self.normalization_time.total_seconds() / 60:.2f} minutes, STD={round(self.normalization_time_STD, 6)}
                            Thread-Mean Line Detection & Data Packaging Time: {self.detection_packaging_time.total_seconds() / 60:.2f} minutes, STD={round(self.detection_packaging_time_STD, 6)}
                            Non-Download Total Mean Elapsed Time: {((self.format_time.total_seconds() + self.normalization_time.total_seconds() + self.detection_packaging_time.total_seconds()) / 60):.2f} minutes
                            Total Elapsed Time: {self.total_time.total_seconds() / 60:.2f} minutes
                            """
            return report
        except Exception as e:
            print('Error occured in time_report: ', e)

    # -----------------------------------------------------------------------------
    def get_times(self):
        """
        Returns a dictionary of exact second times for various processing stages.

        This method provides the elapsed time in seconds for download, formatting,
        normalization, and line detection processes.

        Returns:
            dict: A dictionary containing the elapsed times in seconds for each stage.
        """
        times = {
            'download_time': timedelta(seconds=self.download_time.total_seconds()),
            'format_time': timedelta(seconds=self.format_time.total_seconds()),
            'normalization_time': timedelta(seconds=self.normalization_time.total_seconds()),
            'detection_packaging_time': timedelta(seconds=self.detection_packaging_time.total_seconds())
        }
        return times

    # -----------------------------------------------------------------------------
    def get_norm_spectrum(self):
        """
        Returns the normalized Spectrum1D array.

        Returns:
            list: List of Spectrum1D objects representing normalized spectral data.
        """
        return self.normalized_spectra
    
    # -----------------------------------------------------------------------------
    def get_results(self):
        """
        Returns the analysis results as a QTable.

        Returns:
            QTable: The table containing detected spectral line results.
        """
        return self.results

    # -----------------------------------------------------------------------------
    def get_dict_results(self):
        """
        Returns the analysis results as a dict.

        Returns:
            dict: The dict containing detected spectral line results.
        """
        return self.dict_results

    # -----------------------------------------------------------------------------
    def get_SPARCL_ids(self):
        """
        Returns the list of SPARCL IDs used for data retrieval.

        Returns:
            list: List of SPARCL ID strings.
        """
        return self.SPARCL_ids

    # -----------------------------------------------------------------------------
    def get_client(self):
        """
        Returns the SparclClient instance used for data retrieval.

        Returns:
            SparclClient: The client instance.
        """
        return self.client
       
    # -----------------------------------------------------------------------------
    def set_spectral_resolution_function(self, m: float, b: float):
        """
        Sets the spectral resolution function parameters.

        Args:
            m (float): Slope value for the spectral resolution function.
            b (float): Y-intercept value for the spectral resolution function.

        Returns:
            dict: The updated spectral_resolution_values dictionary.
        """
        self.spectral_resolution_values = {
            "slope" : m,
            "y-intercept" : b
        }
        return self.spectral_resolution_values
    
    def set_SPARCL_ids(self, ids: list, dataset: list = None):
        """
        Sets the SPARCL IDs and optionally the dataset list for analysis.

        This method validates the format of the SPARCL IDs and datasets before setting them.
        
        Args:
            ids (list): List of SPARCL ID strings.
            dataset (list, optional): List of dataset names as strings. Defaults to None.

        Returns:
            None

        Raises:
            ValueError: If the provided ids or dataset are not in the correct format or if an unsupported dataset is provided.
        """
        # Checks for formatting and sets ids
        if not isinstance(ids, list) or not all(isinstance(id, str) for id in ids):
            raise ValueError("SPARCL_ids must be a list of strings.")
        self.SPARCL_ids = ids
        
        # Checks for proper format if dataset is provided
        if dataset is not None:
            if not isinstance(dataset, list) or not all(isinstance(dset, str) for dset in dataset):
                raise ValueError(f'Datasets not provided as a list of strings (e.g., [\'DESI-EDR\']), provided dataset: {dataset}')
            # Checks for supported datasets
            if not all(dset in self.supported_datasets for dset in dataset):
                raise ValueError(f'Unsupported dataset provided, valid datasets are: {self.supported_datasets}')
            self.dataset = dataset

    # =============================================================================
    # Private Helper Methods
    # =============================================================================
    def __download(self):
        """
        Downloads and formats spectral data from the SPARCL database.

        This method retrieves the spectral data for the provided SPARCL IDs, and then formats
        the raw data into an array of Spectrum1D objects. It also handles segmentation of queries
        if more than 500 IDs are provided.

        Returns:
            list: List of Spectrum1D objects containing the formatted spectral data.

        Raises:
            RuntimeError: If an error occurs during data download or formatting.
        """
        # Specifies data to get from SPARCL
        fetch_values = ["wavelength", "redshift", "model"]

        # Monkeypatches the tap function to work in spectrum1d list comprehension
        if self.include_progress_bar:
            Spectrum1D.tap = lambda s, func: (func(s), s)[1]


        # Downloads data from SPARCL
        if len(self.SPARCL_ids) > 500:
            segmentation = True
            chunks = [self.SPARCL_ids[i:i + 500] for i in range(0, len(self.SPARCL_ids), 500)]
            # instantiates the bar
            bar_length = len(chunks)
        else: 
            segmentation = False
            # instantiates the bar
            bar_length = 1
        try:
            start = time.time()
            # With progress bar
            if self.include_progress_bar:
                with alive_bar(bar_length) as bar:
                    if (segmentation):
                        bar.title('Downloading from SPARCL (~500 per batch)')
                        SPARCL_results_array = []
                        for chunk in chunks:
                            SPARCL_results = self.client.retrieve(uuid_list = chunk,
                            dataset_list = self.dataset,
                            include = fetch_values)
                            SPARCL_results_array.append(SPARCL_results)
                            bar()
                    else:
                        bar.title('Downloading from SPARCL (single batch)')
                        SPARCL_results = self.client.retrieve(uuid_list = self.SPARCL_ids,
                        dataset_list = self.dataset,
                        include = fetch_values)
                        bar()
            # Without progress bar
            else:
                if (segmentation):
                    SPARCL_results_array = []
                    for chunk in chunks:
                        SPARCL_results = self.client.retrieve(uuid_list = chunk,
                        dataset_list = self.dataset,
                        include = fetch_values)
                        SPARCL_results_array.append(SPARCL_results)
                else:
                    SPARCL_results = self.client.retrieve(uuid_list = self.SPARCL_ids,
                    dataset_list = self.dataset,
                    include = fetch_values)
        except Exception as e:
            print("Error occured in download(): When downloading data from SPARCL Database: ", e)
        
        # NOTE: Fix to check if response is bad
        # if SPARCL_results_array.records == []:
        #     raise ValueError('API response is empty')

        # Stores download time
        self.download_time = timedelta(seconds=(time.time()-start))


        # Formats all data
        start = time.time()
        try:
            # With progress bar
            if self.include_progress_bar:
                with alive_bar(len(self.SPARCL_ids)) as bar:
                    bar.title('Formatting data into Spectrum1D array')
                    if (segmentation):
                        self.spectrum1d_array = []
                        for result in SPARCL_results_array:
                            self.spectrum1d_array.extend([Spectrum1D(spectral_axis= (record.wavelength / (record.redshift + 1)) * u.AA,
                                flux=np.array(record.model) * u.Unit(self.flux_unit),
                                meta={'sparcl_id' : self.SPARCL_ids[i]}).tap(lambda _: bar())
                                for i, record in enumerate(result.records)])
                    else:
                        self.spectrum1d_array = []
                        for i in np.arange(0, len(SPARCL_results.records), 1):
                            self.spectrum1d_array.append(Spectrum1D(
                                spectral_axis=(SPARCL_results.records[i].wavelength / (SPARCL_results.records[i].redshift + 1)) * u.AA,
                                flux=np.array(SPARCL_results.records[i].model) * u.Unit(self.flux_unit),
                                meta={'sparcl_id': self.SPARCL_ids[i]}
                            ))
                            bar()
            # Without progress bar
            else:
                if (segmentation):
                    self.spectrum1d_array = []
                    for result in SPARCL_results_array:
                        self.spectrum1d_array.extend([Spectrum1D(spectral_axis= (record.wavelength / (record.redshift + 1)) * u.AA,
                            flux=np.array(record.model) * u.Unit(self.flux_unit),
                            meta={'sparcl_id' : self.SPARCL_ids[i]})
                            for i, record in enumerate(result.records)])
                else:
                    self.spectrum1d_array = [Spectrum1D(spectral_axis= (SPARCL_results.records[i].wavelength / (SPARCL_results.records[i].redshift + 1)) * u.AA,
                            flux=np.array(SPARCL_results.records[i].model) * u.Unit(self.flux_unit),
                            meta={'sparcl_id' : self.SPARCL_ids[i]})
                            for i in np.arange(0, len(SPARCL_results.records), 1)]
        except Exception as e:
            print("Error occured in download(): When formatting data from SPARCL Database: ", e)

        self.format_time = timedelta(seconds=(time.time()-start))
        
        # Optionally returns formatted array
        return self.spectrum1d_array

    # -----------------------------------------------------------------------------
    def __set_spectrum1D_array(self, spectra_array):
        """
        __set_spectrum1D_array(self, spectra_array)
        Private method to set the 1D spectrum array for the instance.
        Parameters:
            spectra_array (array-like): The array containing the 1D spectral data to be assigned.
        Returns:
            None
        """
        self.spectrum1d_array = spectra_array

    # -----------------------------------------------------------------------------
    def __median_filter_normalize(self, spectra=None):
        """
        Normalizes the spectra using a median filter.

        This helper function processes the raw Spectrum1D array, applying a median filter
        to compute a continuum and then normalizes the flux values. It raises an error if 
        the spectrum1d_array is not available.

        Args:
            spectra (list, optional): An optional list of Spectrum1D objects. Defaults to None.

        Returns:
            list: List of normalized Spectrum1D objects.
        """
        
        spectra = self.spectrum1d_array
        normalized_flux_array = []
        spectral_axis_array = []

        # Start timer
        start = time.time()

        # Normalization process
        try:
            if self.include_progress_bar and not self.is_thread:
                with alive_bar(len(spectra)) as bar:
                    bar.title('Spectrum normalization')
                    for i in np.arange(0, len(spectra), 1):
                        # Ensures a positive, and non-zero kernel_size - matches to spectrum variability
                        kernel_size = self.__compute_kernel(spec=spectra[i])

                        # normalizes spectrum
                        continuum = median_filter(spectra[i].flux.value, size=int(kernel_size))
                        #To avoid divide by zero error, zero-intercepts are replace by 1 in division
                        continuum[continuum == 0] = 1
                        spectral_axis_array.append(spectra[i].spectral_axis)
                        normalized_flux_array.append(spectra[i].flux / continuum)

                        # Stores normalized spectrum
                        normalized_spectra = [
                        Spectrum1D(
                            spectral_axis=spectral_axis_array[r],
                            flux=normalized_flux_array[r] * u.Unit(self.flux_unit),
                            meta={'sparcl_id': spectra[r].meta['sparcl_id']}
                        )
                        for r in np.arange(0, len(normalized_flux_array), 1)
                        ]
                        bar()
            else:
                for i in np.arange(0, len(spectra), 1):
                    # Ensures a positive, and non-zero kernel_size - matches to spectrum variability
                    kernel_size = self.__compute_kernel(spec=spectra[i])

                    # normalizes spectrum
                    continuum = median_filter(spectra[i].flux.value, size=int(kernel_size))
                    #To avoid divide by zero error, zero-intercepts are replace by 1 in division
                    continuum[continuum == 0] = 1
                    spectral_axis_array.append(spectra[i].spectral_axis)
                    normalized_flux_array.append(spectra[i].flux / continuum)

                    # Stores normalized spectrum
                    normalized_spectra = [
                    Spectrum1D(
                        spectral_axis=spectral_axis_array[r],
                        flux=normalized_flux_array[r] * u.Unit(self.flux_unit),
                        meta={'sparcl_id': spectra[r].meta['sparcl_id']}
                    )
                    for r in np.arange(0, len(normalized_flux_array), 1)
                    ]

        except Exception as e:
            print('Error occured in __median_filter_normalize(), when normalizing spectrum.:', e)

        self.normalized_spectra = normalized_spectra

        # Store time value
        self.normalization_time = timedelta(seconds=(time.time() - start))

        # optionally returns normalized_flux_array
        return normalized_spectra

    # -----------------------------------------------------------------------------
    def __find_closest_in_range(self, line, minv, maxv):
        """
        INCLUSIVE SEARCH

        Returns the index of the closest defined wavelength within the range [minv, maxv].

        Args:
            line: The reference wavelength value.
            minv: The minimum wavelength value in the range.
            maxv: The maximum wavelength value in the range.

        Returns:
            int or None: The index of the closest wavelength in range, or None if no value is found.
        """
        try:
            left_index = bisect.bisect_left(self.line_wavelengths, minv)
            right_index = bisect.bisect_right(self.line_wavelengths, maxv)

            # Return None if no values are in range
            if left_index == right_index:
                return None

            # Find the closest value to 'line' in the range
            closest_index = min(range(left_index, right_index), key=lambda i: abs(self.line_wavelengths[i] - line))
            return closest_index
        except Exception as e:
            print('Error occured in __find_closest_in_range(): ', e)
    
    # -----------------------------------------------------------------------------
    def __find_closest(self, array, value):
        """
        Returns the index of the closest value in the array to the given value.

        Assumes the array is sorted for computational efficiency.

        Args:
            array (list): Sorted list of numerical values.
            value (float): The reference value to compare.

        Returns:
            int: Index of the closest value in the array.
        """
        try:
            pos = bisect.bisect_left(array, value)
            if pos == 0:
                return 0
            if pos == len(array):
                return len(array) - 1
            before = pos - 1
            after = pos
            if abs(array[after] - value) < abs(array[before] - value):
                return after
            else:
                return before
        except Exception as e:
            print('Error occured in __find_closest(): ', e)

    # -----------------------------------------------------------------------------
    def __line_detect(self):
        """
        Performs spectral line detection on normalized spectra.

        This method iterates over each normalized spectrum, detects spectral lines
        using the `find_lines_derivative` function, and matches these detected lines
        with known emission lines from the predefined database. The results include
        detailed information about each detected line such as flux, wavelength, resolution,
        and associated metadata.

        Returns:
            dict: A table containing the detected spectral line information for each spectrum.
                Appends th Qtable to self.results

        Raises:
            RuntimeError: If an error occurs during line detection or matching.
        """
        dict_collection = {
            "id" : self.SPARCL_ids.copy(),
            "data" : []
        }
        # http://astronomy.nmsu.edu/drewski/tableofemissionlines.html
        
        # Suppresses high SNR warning
        specutils.conf.do_continuum_function_check = False

        # Itterates over each normalized spectra, detecting lines for each
        # With progress bar
        if self.include_progress_bar and not self.is_thread:
            with alive_bar(len(self.normalized_spectra)) as bar:
                bar.title('Line detection and data packaging')
                for i in range(len(self.normalized_spectra)):
                    # Determines list of possible lines from find_lines_derivative
                        # ignores high SNR warnings from find_lines_derivative
                    try:
                        with warnings.catch_warnings():
                            warnings.simplefilter('ignore')
                            lines_qt = find_lines_derivative(self.normalized_spectra[i], flux_threshold=None)
                            detected_lines = lines_qt['line_center'].value
                            line_types = lines_qt['line_type']
                    except Exception as e:
                        print(f'Unknown error occuring in line_detect(), find_lines_derivative portion on loop {i}: ', e)
                    
                    flagged_line_info = {
                        "indicies" : [],
                        "line_flux" : [],
                        "def_line_wavelength" : [],
                        "obs_line_wavelength" : [],
                        "line_resolution" : [],
                        "line_type" : [],
                        "spectrum_index" : [],
                        "line_deviation" : [],
                        "ion" : [],
                        "Ei" : [],
                        "Ek" : [],
                        "configuration" : [],
                        "terms" : [],
                        "Ji-Jk" : [],
                        "type" : [],
                        "creation_IP" : [],
                        "observation_reference" : [],
                        "Wolf-Rayet_feature" : []
                    }

                    # Matches possible lines with defined wavelengths and collects flux in one pass
                    for m in range(len(detected_lines)):
                        # Determines if uncertainty is within DESI-EDR telescope uncertainties
                        spectral_resolution = (detected_lines[m] * self.spectral_resolution_values['slope'] + self.spectral_resolution_values['y-intercept'])
                        
                        ang_max = detected_lines[m] + spectral_resolution
                        ang_min = detected_lines[m] - spectral_resolution

                        try:
                            # Collects the closest line within the spectral resolution range
                            flag_index = self.__find_closest_in_range(detected_lines[m], ang_min, ang_max)
                            # only appends if the line has not been found before
                            if flag_index is not None and flag_index not in flagged_line_info['indicies']:
                                # Matches the detected line with the closest match in the observed spectra
                                observed_match_index = self.__find_closest(self.normalized_spectra[i].spectral_axis.value, self.line_wavelengths[flag_index])
                                observed_flux = self.spectrum1d_array[i].flux[observed_match_index]
                                
                                def_wavelength = self.line_wavelengths[flag_index]
                                # Adding all desired values to array
                                flagged_line_info['line_resolution'].append(float(spectral_resolution))
                                flagged_line_info['indicies'].append(flag_index)
                                flagged_line_info['line_flux'].append(observed_flux)
                                flagged_line_info['def_line_wavelength'].append(def_wavelength)
                                flagged_line_info['line_type'].append(line_types[m])
                                flagged_line_info['obs_line_wavelength'].append(float(detected_lines[m]))
                                flagged_line_info['spectrum_index'].append(observed_match_index)
                                flagged_line_info['line_deviation'].append(float(detected_lines[m]-def_wavelength))
                        except Exception as e:
                            print(f"Unknown error occuring in __line_detect(), during line-matching process: spectra of index {i}: ", e)
                    
                    try:
                        # Itterates over indexes to grab desired values from line_info
                        for wavelength in flagged_line_info['def_line_wavelength']:
                            line = self.lines_info[str(wavelength)]
                            flagged_line_info['ion'].append(line[0])
                            flagged_line_info['Ei'].append(float(line[1]) if line[1] != "" else 0)
                            flagged_line_info['Ek'].append(float(line[2]) if line[2] != "" else 0)
                            flagged_line_info['configuration'].append(line[3])
                            flagged_line_info['terms'].append(line[4])
                            flagged_line_info['Ji-Jk'].append(line[5])
                            flagged_line_info['type'].append(line[6])
                            flagged_line_info['creation_IP'].append(float(line[7]) if line[7] != "" else 0)
                            flagged_line_info['observation_reference'].append(line[8])
                            flagged_line_info['Wolf-Rayet_feature'].append(line[9])


                        # Package date from single spectra
                        qt = QTable({   
                            "line_wavelength" : flagged_line_info['def_line_wavelength'] * u.AA,
                            "observed_wavelength" : flagged_line_info['obs_line_wavelength'] * u.AA,
                            "line_type" : flagged_line_info['line_type'],
                            "line_flux" : flagged_line_info['line_flux'] * u.Unit(self.flux_unit),
                            "line_deviation" : flagged_line_info['line_deviation'] * u.AA,
                            "line_resolution" : flagged_line_info['line_resolution'] * u.AA,
                            "spectrum_index": flagged_line_info['spectrum_index'],
                            "ion" : flagged_line_info['ion'],
                            "Ei" :  flagged_line_info['Ei'] * u.eV,
                            "Ek" : flagged_line_info['Ek'] * u.eV,
                            "configuration" : flagged_line_info['configuration'],
                            "terms" : flagged_line_info['terms'],
                            "Ji-Jk" : flagged_line_info['creation_IP'],
                            "type" : flagged_line_info['type'],
                            "creation_IP" : flagged_line_info['creation_IP'] *u.eV,
                            "obseration_reference" : flagged_line_info['observation_reference'],
                            "Wolf-Rayet_feature" : flagged_line_info['Wolf-Rayet_feature']
                        },
                        names=["line_wavelength",
                            "observed_wavelength",
                            "line_type",
                            "line_flux",
                            "line_deviation",
                            "line_resolution",
                            "spectrum_index",
                            "ion",
                            "Ei",
                            "Ek",
                            "configuration",
                            "terms",
                            "Ji-Jk",
                            "type",
                            "creation_IP",
                            "obseration_reference",
                            "Wolf-Rayet_feature"],
                        dtype=['astropy.units.quantity.Quantity',
                            'astropy.units.quantity.Quantity',
                            'str',
                            'astropy.units.quantity.Quantity',
                            'astropy.units.quantity.Quantity',
                            'astropy.units.quantity.Quantity',
                            'int',
                            'str',
                            'astropy.units.quantity.Quantity',
                            'astropy.units.quantity.Quantity',
                            'str',
                            'str',
                            'str',
                            'str',
                            'astropy.units.quantity.Quantity',
                            'str',
                            'bool'])
                        dict_collection['data'].append(qt)

                    # Catches any excpetions
                    except Exception as e:
                        print('Error occured in __line_detect(), when packaging data: ', e)
                    # Finally updates bar
                    finally:
                        bar()
        # Without progress bar
        else:
            for i in range(len(self.normalized_spectra)):
                # Determines list of possible lines from find_lines_derivative
                    # ignores high SNR warnings from find_lines_derivative
                try:
                    lines_qt = find_lines_derivative(self.normalized_spectra[i], flux_threshold=None)
                    detected_lines = lines_qt['line_center'].value
                    line_types = lines_qt['line_type']
                except Exception as e:
                    print(f'Unknown error occuring in line_detect(), find_lines_derivative portion on loop {i}: ', e)
                
                flagged_line_info = {
                    "indicies" : [],
                    "line_flux" : [],
                    "def_line_wavelength" : [],
                    "obs_line_wavelength" : [],
                    "line_resolution" : [],
                    "line_type" : [],
                    "spectrum_index" : [],
                    "line_deviation" : [],
                    "ion" : [],
                    "Ei" : [],
                    "Ek" : [],
                    "configuration" : [],
                    "terms" : [],
                    "Ji-Jk" : [],
                    "type" : [],
                    "creation_IP" : [],
                    "observation_reference" : [],
                    "Wolf-Rayet_feature" : []
                }

                # Matches possible lines with defined wavelengths and collects flux in one pass
                for m in range(len(detected_lines)):
                    # Determines if uncertainty is within DESI-EDR telescope uncertainties
                    spectral_resolution = (detected_lines[m] * self.spectral_resolution_values['slope'] + self.spectral_resolution_values['y-intercept'])
                    
                    ang_max = detected_lines[m] + spectral_resolution
                    ang_min = detected_lines[m] - spectral_resolution

                    try:
                        # Collects the closest line within the spectral resolution range
                        flag_index = self.__find_closest_in_range(detected_lines[m], ang_min, ang_max)
                        # only appends if the line has not been found before
                        if flag_index is not None and flag_index not in flagged_line_info['indicies']:
                            # Matches the detected line with the closest match in the observed spectra
                            observed_match_index = self.__find_closest(self.normalized_spectra[i].spectral_axis.value, self.line_wavelengths[flag_index])
                            observed_flux = self.spectrum1d_array[i].flux[observed_match_index]
                            
                            def_wavelength = self.line_wavelengths[flag_index]
                            # Adding all desired values to array
                            flagged_line_info['line_resolution'].append(float(spectral_resolution))
                            flagged_line_info['indicies'].append(flag_index)
                            flagged_line_info['line_flux'].append(observed_flux)
                            flagged_line_info['def_line_wavelength'].append(def_wavelength)
                            flagged_line_info['line_type'].append(line_types[m])
                            flagged_line_info['obs_line_wavelength'].append(float(detected_lines[m]))
                            flagged_line_info['spectrum_index'].append(observed_match_index)
                            flagged_line_info['line_deviation'].append(float(detected_lines[m]-def_wavelength))
                    except Exception as e:
                        print(f"Unknown error occuring in __line_detect(), during line-matching process: spectra of index {i}: ", e)
                
                try:
                    # Itterates over indexes to grab desired values from line_info
                    for wavelength in flagged_line_info['def_line_wavelength']:
                        line = self.lines_info[str(wavelength)]
                        flagged_line_info['ion'].append(line[0])
                        flagged_line_info['Ei'].append(float(line[1]) if line[1] != "" else 0)
                        flagged_line_info['Ek'].append(float(line[2]) if line[2] != "" else 0)
                        flagged_line_info['configuration'].append(line[3])
                        flagged_line_info['terms'].append(line[4])
                        flagged_line_info['Ji-Jk'].append(line[5])
                        flagged_line_info['type'].append(line[6])
                        flagged_line_info['creation_IP'].append(float(line[7]) if line[7] != "" else 0)
                        flagged_line_info['observation_reference'].append(line[8])
                        flagged_line_info['Wolf-Rayet_feature'].append(line[9])


                    # Package date from single spectra
                    qt = QTable({   
                        "line_wavelength" : flagged_line_info['def_line_wavelength'] * u.AA,
                        "observed_wavelength" : flagged_line_info['obs_line_wavelength'] * u.AA,
                        "line_type" : flagged_line_info['line_type'],
                        "line_flux" : flagged_line_info['line_flux'] * u.Unit(self.flux_unit),
                        "line_deviation" : flagged_line_info['line_deviation'] * u.AA,
                        "line_resolution" : flagged_line_info['line_resolution'] * u.AA,
                        "spectrum_index": flagged_line_info['spectrum_index'],
                        "ion" : flagged_line_info['ion'],
                        "Ei" :  flagged_line_info['Ei'] * u.eV,
                        "Ek" : flagged_line_info['Ek'] * u.eV,
                        "configuration" : flagged_line_info['configuration'],
                        "terms" : flagged_line_info['terms'],
                        "Ji-Jk" : flagged_line_info['creation_IP'],
                        "type" : flagged_line_info['type'],
                        "creation_IP" : flagged_line_info['creation_IP'] *u.eV,
                        "obseration_reference" : flagged_line_info['observation_reference'],
                        "Wolf-Rayet_feature" : flagged_line_info['Wolf-Rayet_feature']
                    },
                    names=["line_wavelength",
                        "observed_wavelength",
                        "line_type",
                        "line_flux",
                        "line_deviation",
                        "line_resolution",
                        "spectrum_index",
                        "ion",
                        "Ei",
                        "Ek",
                        "configuration",
                        "terms",
                        "Ji-Jk",
                        "type",
                        "creation_IP",
                        "obseration_reference",
                        "Wolf-Rayet_feature"],
                    dtype=['astropy.units.quantity.Quantity',
                        'astropy.units.quantity.Quantity',
                        'str',
                        'astropy.units.quantity.Quantity',
                        'astropy.units.quantity.Quantity',
                        'astropy.units.quantity.Quantity',
                        'int',
                        'str',
                        'astropy.units.quantity.Quantity',
                        'astropy.units.quantity.Quantity',
                        'str',
                        'str',
                        'str',
                        'str',
                        'astropy.units.quantity.Quantity',
                        'str',
                        'bool'])
                    dict_collection['data'].append(qt)
                except Exception as e:
                    print('Error occured in __line_detect(), when packaging data: ', e)

        # saves QTable
        self.results = QTable(dict_collection)
        self.dict_results = dict_collection

        # optionally returns dict
        return dict_collection

    # -----------------------------------------------------------------------------
    # NOTE: batch for more than 5000 ids (SPARCL limit)
    # NOTE: implement bar support
    def __get_test_ids(self, limit: int):
        """
        Retrieves a specified number of test SPARCL IDs and sets them for analysis.

        This method queries the SPARCL database for test records based on constraints,
        extracts the SPARCL IDs, and sets them for the current instance.

        Args:
            limit (int): The maximum number of SPARCL IDs to retrieve.

        Returns:
            tuple: A tuple containing the list of SPARCL IDs and the dataset list.
        """
        try:
            dataset_list = ['DESI-EDR']
            cont = {'spectype' : ['GALAXY'], 'data_release' : dataset_list}
            outf = ['sparcl_id']
            response = self.client.find(constraints=cont,
                            outfields=outf,
                            limit=limit)
            sparcl_ids = ['%s' % (s.sparcl_id) for s in response.records]

            self.set_SPARCL_ids(sparcl_ids, dataset_list)

            return sparcl_ids, dataset_list
        except Exception as e:
            print('Error occured in __get_test_ids(): ', e)

    # -----------------------------------------------------------------------------
    # NOTE: add functionality for non-SPARCL/EDR data
    def __singlethreaded_analyze(self, is_thread=False):
        """
        Performs a single-threaded analysis of the spectral data.

        This private method runs the download, normalization, and spectral line detection
        sequentially on the current set of SPARCL IDs.

        Returns:
            None

        Raises:
            AttributeError: If no SPARCL IDs are provided.
        """

        # runs individual functions to process into class vars
        if not is_thread:
            self.__download()

        start = time.time()
        self.__median_filter_normalize()
        self.normalization_time = timedelta(seconds=(time.time() - start))

        start = time.time()
        self.__line_detect()
        self.detection_packaging_time = timedelta(seconds=(time.time() - start))

        return

    # -----------------------------------------------------------------------------
    def __multithreaded_analyze(self):
        """
        Executes a multithreaded analysis using a thread pool executor.

        This method creates a thread pool based on the allocated thread count, and submits
        each SPEAR instance from `thread_classes` to be processed in parallel using the worker method.

        Returns:
            list: The list of SPEAR instances after processing.
        """
        try:
            pool = concurrent.futures.ThreadPoolExecutor(max_workers=self.thread_allocation)
        except Exception as e:
            print('Error occured in __multithreaded_analyze(), when assigning workers to pool: ', e)
        for thread_class in self.thread_classes:
            pool.submit(self.__worker, thread_class)

        pool.shutdown(wait=True)

        times_array = [[], []]  # Initialize as a list of lists to store multiple timedelta objects
        # concatenates data from threads into final result:
        for i in range(len(self.thread_classes)):
            # Appends processing time across threads
            times = self.thread_classes[i].get_times()
            times_array[0].append(times['normalization_time'])
            times_array[1].append(times['detection_packaging_time'])

            # Appends data from each thread
            new_dict_results = self.thread_classes[i].get_dict_results()
            if i == 0:
                dict_results = new_dict_results
            else:
                if new_dict_results == None:
                    raise ValueError('Thread returned None as a result in __multithreaded_analyze')
                dict_results ={
                    'id' : dict_results.get('id', []) + new_dict_results.get('id', []),
                    'data' : dict_results.get('data', []) + new_dict_results.get('data', [])
                }
        
        # Sets average times for threading
        self.normalization_time = np.mean(times_array[0])
        self.detection_packaging_time = np.mean(times_array[1])
        self.normalization_time_STD = np.std([t.total_seconds() for t in times_array[0]])
        self.detection_packaging_time_STD = np.std([t.total_seconds() for t in times_array[1]])
        self.results = QTable(dict_results)
        self.total_time = timedelta(seconds=(time.time() - self.start_time))

        return self.thread_classes

    # -----------------------------------------------------------------------------
    def __worker(self, spear):
        """
        Worker function for multithreaded analysis.

        This function is executed in a separate thread for each SPEAR instance.
        It performs single-threaded analysis on the provided SPEAR instance.

        Args:
            spear (SPEAR): An instance of the SPEAR class to be analyzed.

        Returns:
            QTable: The analysis results for the given SPEAR instance.
        """

        spear.__singlethreaded_analyze(is_thread=True)
        results = spear.get_dict_results()
        return results

    # -----------------------------------------------------------------------------
    def __compute_kernel(self, spec, desired_window: u.Quantity = 100*u.AA):
        """
        Computes the kernel size for median filtering based on a desired physical smoothing window.

        The kernel size is derived by estimating the representative wavelength step from the median
        of the differences between successive wavelengths. This allows the smoothing window to be
        adapted even for non-uniformly spaced spectral data.

        Args:
            spec (Spectrum1D): A DESI-EDR spectrum whose spectral_axis is used to compute the kernel size.
            desired_window (astropy.units.Quantity, optional): The desired smoothing window for the continuum in Angstrom.
                                                             Defaults to 100 Å.

        Returns:
            int: The computed kernel size (an odd integer) to be used for the median filter.
        """
        try:
            # Convert wavelengths to Angstrom and get as a numpy array
            wavelengths = spec.spectral_axis.value

            # Compute differences between successive wavelengths
            delta_wavelengths = np.diff(wavelengths)
            if len(delta_wavelengths) == 0:
                raise ValueError("Spectrum wavelength array must have more than one element.")
            
            # Use the median of the differences as the representative step size
            median_step = np.median(delta_wavelengths)

            # Calculate kernel size: number of pixels that span the desired physical window
            kernel_size = int(np.ceil(desired_window.to(u.AA).value / median_step))

            # Enforce a minimum kernel size of 1 and adjust to be odd for symmetric filtering
            kernel_size = max(kernel_size, 1)
            if kernel_size % 2 == 0:
                kernel_size += 1

            return kernel_size
        except Exception as e:
            print('Error occured in __compute_kernel: ', e)


    def __tap(self, func):
        func(self)
        return self