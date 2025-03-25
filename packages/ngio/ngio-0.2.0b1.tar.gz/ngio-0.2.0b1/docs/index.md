# Welcome to NGIO

NGIO is a Python library to streamline OME-Zarr image analysis workflows.

**Main Goals:**

- Abstract object base API for handling OME-Zarr files
- Powefull iterators for processing data using common access patterns
- Tight integration with [Fractal's Table Fractal](https://fractal-analytics-platform.github.io/fractal-tasks-core/tables/)
- Validate OME-Zarr files

To get started, check out the [Getting Started](getting-started.md) guide.

## 🚧 Ngio is Under active Development 🚧

### Roadmap

| Feature | Status | ETA | Description |
|---------|--------|-----|-------------|
| Metadata Handling | ✅ | | Read, Write, Validate OME-Zarr Metadata (0.4 supported, 0.5 ready) |
| OME-Zarr Validation | ✅ | | Validate OME-Zarr files for compliance with the OME-Zarr Specification + Compliance between Metadata and Data |
| Base Image Handling | ✅ | | Load data from OME-Zarr files, retrieve basic metadata, and write data |
| ROI Handling | ✅ | | Common ROI models |
| Label Handling | ✅ | Mid-September | Based on Image Handling |
| Table Validation | ✅ | Mid-September | Validate Table fractal V1 + Compliance between Metadata and Data |
| Table Handling | ✅ | Mid-September | Read, Write ROI, Features, and Masked Tables |
| Basic Iterators | Ongoing | End-September | Read and Write Iterators for common access patterns |
| Base Documentation | ✅ | End-September | API Documentation and Examples |
| Beta Ready Testing | ✅ | End-September | Beta Testing; Library is ready for testing, but the API is not stable |
| Streaming from Fractal | Ongoing | December | Ngio can stream ome-zarr from fractal |
| Mask Iterators | Ongoing | Early 2025 | Iterators over Masked Tables |
| Advanced Iterators | Not started | mid-2025 | Iterators for advanced access patterns |
| Parallel Iterators | Not started | mid-2025 | Concurrent Iterators for parallel read and write |
| Full Documentation | Not started | 2025 | Complete Documentation |
| Release 1.0 (Commitment to API) | Not started | 2025 | API is stable; breaking changes will be avoided |

## Contributors

`ngio` is developed at the [BioVisionCenter](https://www.biovisioncenter.uzh.ch/en.html) at the University of Zurich. The main contributors are: [@lorenzocerrone](https://github.com/lorenzocerrone), [@jluethi](https://github.com/jluethi).

## License

`ngio` is released according to the BSD-3-Clause License. See [LICENSE](https://github.com/fractal-analytics-platform/ngio/blob/main/LICENSE)
