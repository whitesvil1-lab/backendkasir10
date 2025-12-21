-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 21, 2025 at 08:12 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_kasir1`
--

-- --------------------------------------------------------

--
-- Table structure for table `google_users`
--

CREATE TABLE `google_users` (
  `id` int(2) NOT NULL,
  `email` varchar(100) NOT NULL,
  `verified` varchar(10) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `google_users`
--

INSERT INTO `google_users` (`id`, `email`, `verified`, `created_at`) VALUES
(1, 'nabilvictar@gmail.com', '', '2025-12-19 14:00:54');

-- --------------------------------------------------------

--
-- Table structure for table `produk_biasa`
--

CREATE TABLE `produk_biasa` (
  `no_SKU` int(11) NOT NULL,
  `Name_product` varchar(100) NOT NULL,
  `expired_date` date NOT NULL,
  `Price` int(11) NOT NULL,
  `stok` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `produk_biasa`
--

INSERT INTO `produk_biasa` (`no_SKU`, `Name_product`, `expired_date`, `Price`, `stok`) VALUES
(1, 'TEAJUS GULA BATU 1 RENCENG', '2026-11-26', 6000, 9),
(2, 'NABATI KEJU 200GR', '2026-12-28', 2000, 0),
(3, 'KAIN PEL ', '2029-02-02', 10000, 9),
(4, 'SOSIS SONICE', '2027-10-10', 1000, 10),
(5, 'GOOD DAY FREEZE SASCHET', '2026-11-11', 2000, 2);

-- --------------------------------------------------------

--
-- Table structure for table `produk_lelang`
--

CREATE TABLE `produk_lelang` (
  `no_SKU` int(10) NOT NULL,
  `Name_product` varchar(100) NOT NULL,
  `expired_date` datetime NOT NULL,
  `Price` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `google_user_id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('admin','kasir','staff','') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `google_user_id`, `username`, `password_hash`, `role`) VALUES
(2, 1, 'nabil', 'nabil123', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `google_users`
--
ALTER TABLE `google_users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `produk_lelang`
--
ALTER TABLE `produk_lelang`
  ADD PRIMARY KEY (`no_SKU`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `google_user_id` (`google_user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `google_users`
--
ALTER TABLE `google_users`
  MODIFY `id` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `produk_lelang`
--
ALTER TABLE `produk_lelang`
  MODIFY `no_SKU` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `fk_users_google` FOREIGN KEY (`google_user_id`) REFERENCES `google_users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
