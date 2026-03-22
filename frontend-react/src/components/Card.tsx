import { motion } from "framer-motion";

type Props = {
  children: React.ReactNode;
};

export default function Card({ children }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25 }}
      className="rounded-2xl border bg-white p-6 shadow-sm transition hover:shadow-md dark:border-gray-700 dark:bg-gray-800"
    >
      {children}
    </motion.div>
  );
}